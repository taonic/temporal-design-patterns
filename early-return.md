### Update With Start (Early Return)

#### Intent
Return initialization results to the caller immediately while continuing asynchronous processing in the background.

#### Problem
Clients need immediate feedback on whether an operation can proceed, but the full operation takes significant time to complete. Blocking the client for the entire operation duration creates poor user experience and ties up resources.

#### Solution
Uses Update-with-Start to split operations into two phases: a fast synchronous initialization phase that validates and returns results immediately, and a slower asynchronous completion phase that runs in the background. The workflow uses local activities for quick initialization, signals completion via update handlers, then either completes or cancels the operation based on initialization success.

**Go Implementation:**
```go
func Workflow(ctx workflow.Context, txRequest TransactionRequest) (*Transaction, error) {
    var tx *Transaction
    var initDone bool
    var initErr error

    // Register update handler that waits for initialization
    workflow.SetUpdateHandler(ctx, UpdateName,
        func(ctx workflow.Context) (*Transaction, error) {
            workflow.Await(ctx, func() bool { return initDone })
            return tx, initErr
        },
    )

    // Phase 1: Fast synchronous initialization (local activity)
    localOpts := workflow.WithLocalActivityOptions(ctx, workflow.LocalActivityOptions{
        ScheduleToCloseTimeout: 5 * time.Second,
    })
    initErr = workflow.ExecuteLocalActivity(localOpts, txRequest.Init).Get(ctx, &tx)
    initDone = true // Signal update handler

    // Phase 2: Slow asynchronous completion
    activityCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
        StartToCloseTimeout: 30 * time.Second,
    })

    if initErr != nil {
        // Cancel on initialization failure
        return nil, workflow.ExecuteActivity(activityCtx, CancelTransaction, tx).Get(ctx, nil)
    }

    // Complete on initialization success
    return tx, workflow.ExecuteActivity(activityCtx, CompleteTransaction, tx).Get(ctx, nil)
}
```
[Complete Go Sample](https://github.com/temporalio/samples-go/tree/main/early-return)

**Java Implementation:**
```java
public class TransactionWorkflowImpl implements TransactionWorkflow {
    private boolean initDone = false;
    private Transaction tx;
    private Exception initError = null;

    @Override
    public TxResult processTransaction(TransactionRequest txRequest) {
        this.tx = activities.mintTransactionId(txRequest);

        // Phase 1: Fast synchronous initialization
        try {
            this.tx = activities.initTransaction(this.tx);
        } catch (Exception e) {
            initError = e;
        } finally {
            initDone = true; // Signal update handler
        }

        // Phase 2: Slow asynchronous completion
        if (initError != null) {
            activities.cancelTransaction(this.tx);
            return new TxResult("", "Transaction cancelled.");
        } else {
            activities.completeTransaction(this.tx);
            return new TxResult(this.tx.getId(), "Transaction completed successfully.");
        }
    }

    @Override
    public TxResult returnInitResult() {
        Workflow.await(() -> initDone); // Wait for initialization
        if (initError != null) {
            throw Workflow.wrap(initError);
        }
        return new TxResult(tx.getId(), "Initialization successful");
    }
}
```
[Complete Java Sample](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/earlyreturn)

**Key Differences:**
- **Go**: Uses SetUpdateHandler with closure capturing variables
- **Java**: Uses separate update method (returnInitResult) with instance variables
- **Both**: Use Workflow.await() to block until initialization completes
- **Both**: Return initialization result immediately while processing continues

#### Applicability
Use this pattern when:
- Clients need immediate feedback but operations take time to complete
- Validation or initialization can be done quickly (< 5 seconds)
- The operation can be safely cancelled if initialization fails
- You want to avoid blocking clients during long-running processing
- The initialization result determines whether to proceed or abort

#### Additional Use Cases

**1. E-commerce Payment Processing**
```go
// Return payment authorization immediately while processing settlement
func PaymentWorkflow(ctx workflow.Context, payment PaymentRequest) (*PaymentAuth, error) {
    var auth *PaymentAuth
    var authDone bool
    
    workflow.SetUpdateHandler(ctx, "GetAuthResult",
        func(ctx workflow.Context) (*PaymentAuth, error) {
            workflow.Await(ctx, func() bool { return authDone })
            return auth, nil
        },
    )
    
    // Fast authorization check (local activity)
    localCtx := workflow.WithLocalActivityOptions(ctx, workflow.LocalActivityOptions{
        ScheduleToCloseTimeout: 3 * time.Second,
    })
    err := workflow.ExecuteLocalActivity(localCtx, AuthorizePayment, payment).Get(ctx, &auth)
    authDone = true
    
    if err != nil {
        return nil, workflow.ExecuteActivity(ctx, CancelPayment, payment).Get(ctx, nil)
    }
    
    // Background settlement processing
    return auth, workflow.ExecuteActivity(ctx, SettlePayment, auth).Get(ctx, nil)
}
```

**2. User Onboarding & KYC Verification**
- Quick identity validation returns user ID immediately
- Background processes handle document verification, credit checks, and account setup
- Client can proceed with basic user experience while onboarding completes

**3. Resource Provisioning (Cloud/Infrastructure)**
```java
@Override
public ProvisionResult provisionInfrastructure(ProvisionRequest request) {
    boolean validationDone = false;
    ResourceValidation validation = null;
    
    // Fast resource validation (quotas, permissions, etc.)
    try {
        validation = activities.validateResources(request);
        validationDone = true;
    } catch (Exception e) {
        validationDone = true;
        throw e;
    }
    
    if (validation.hasErrors()) {
        activities.cleanupResources(validation.getResourceIds());
        return new ProvisionResult("", "Validation failed: " + validation.getErrors());
    }
    
    // Long-running provisioning (VMs, databases, networking)
    activities.provisionCompute(validation);
    activities.configureNetworking(validation);
    activities.setupMonitoring(validation);
    
    return new ProvisionResult(validation.getResourceId(), "Provisioned successfully");
}

@Override
public ResourceValidation getValidationResult() {
    Workflow.await(() -> validationDone);
    return validation;
}
```

**4. Document Processing & Approval Workflows**
- Immediate receipt confirmation with document ID
- Background OCR processing, content analysis, and routing to approvers
- Users can track progress without waiting for full processing

**5. AI/ML Model Training & Inference**
```go
func MLModelWorkflow(ctx workflow.Context, req TrainingRequest) (*ModelMetadata, error) {
    var metadata *ModelMetadata
    var setupDone bool
    
    workflow.SetUpdateHandler(ctx, "GetModelInfo",
        func(ctx workflow.Context) (*ModelMetadata, error) {
            workflow.Await(ctx, func() bool { return setupDone })
            return metadata, nil
        },
    )
    
    // Quick setup: validate data, allocate resources, start training
    localCtx := workflow.WithLocalActivityOptions(ctx, workflow.LocalActivityOptions{
        ScheduleToCloseTimeout: 10 * time.Second,
    })
    err := workflow.ExecuteLocalActivity(localCtx, SetupTraining, req).Get(ctx, &metadata)
    setupDone = true
    
    if err != nil {
        return nil, err
    }
    
    // Long-running training and evaluation
    activityCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
        StartToCloseTimeout: 6 * time.Hour, // Long training time
    })
    
    return metadata, workflow.ExecuteActivity(activityCtx, TrainAndEvaluateModel, metadata).Get(ctx, nil)
}
```

**6. Order Processing with Inventory Check**
- Fast inventory availability check returns order confirmation
- Background fulfillment includes picking, packing, and shipping
- Customer gets immediate order confirmation while processing continues

**7. Multi-step Financial Transactions**
- Quick fraud detection and initial authorization
- Background compliance checks, risk assessment, and final settlement
- Critical for high-frequency trading or payment processing

**8. Content Publishing & Moderation**
- Immediate publish with content ID after basic validation
- Background content analysis, moderation, and optimization
- Authors can share content immediately while safety checks continue

**Performance Benefits:**
- Latency reduction of 40-50% compared to synchronous processing
- Can achieve up to 91% improvement when combined with Local Activities
- Measured improvements from 850ms to 265ms in payment processing scenarios

#### Pros
- ✅ Immediate client feedback via Update-with-Start in single round trip
- ✅ Non-blocking - clients don't wait for full operation completion
- ✅ Local activities avoid extra server roundtrips during initialization
- ✅ Clear separation between validation and execution phases
- ✅ Automatic cancellation handling on initialization failure

#### Cons
- ❌ Requires careful timeout tuning for local activities
- ❌ Clients must handle asynchronous completion separately
- ❌ More complex than simple synchronous workflows
- ❌ Initialization must complete within a single workflow task
- ❌ Limited to operations that can be split into fast/slow phases

#### Relations with Other Patterns
- Uses **Local Activities** for fast initialization without server roundtrips
- Can combine with **Saga Pattern** to add compensation for failed completions
- Often paired with **Signals** or **Queries** for clients to check completion status
- May use **Async Activity Completion** for external system integration in phase 2
