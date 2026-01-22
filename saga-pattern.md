# Saga Pattern

[Go Sample](https://github.com/temporalio/samples-go/tree/main/saga)  
[Java Sample](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/hello/HelloSaga.java)

## Intent
Manage distributed transactions across multiple services by coordinating a sequence of local transactions, each with a compensating action that can undo its effects if subsequent steps fail.

## Problem
In distributed systems, you need to maintain data consistency across multiple services or databases without using traditional ACID transactions. When a multi-step business process fails partway through, you must undo the effects of completed steps to maintain system consistency. Traditional two-phase commit doesn't scale well and creates tight coupling between services.

## Solution
Implement each step as a local transaction with a corresponding compensation transaction. If any step fails, execute compensation transactions in reverse order to undo the effects of all completed steps. Use Go's `defer` mechanism to automatically trigger compensations when errors occur, ensuring cleanup happens even if the workflow logic panics or returns early.

## Structure

**Go Implementation** (using `defer`):
```go
func TransferMoney(ctx workflow.Context, details TransferDetails) error {
    // Step 1: Withdraw from source account
    err := workflow.ExecuteActivity(ctx, Withdraw, details).Get(ctx, nil)
    if err != nil {
        return err
    }
    
    // Register compensation for Step 1
    defer func() {
        if err != nil {
            _ = workflow.ExecuteActivity(ctx, WithdrawCompensation, details).Get(ctx, nil)
        }
    }()
    
    // Step 2: Deposit to target account
    err = workflow.ExecuteActivity(ctx, Deposit, details).Get(ctx, nil)
    if err != nil {
        return err // Triggers defer, which runs WithdrawCompensation
    }
    
    // Register compensation for Step 2
    defer func() {
        if err != nil {
            _ = workflow.ExecuteActivity(ctx, DepositCompensation, details).Get(ctx, nil)
        }
    }()
    
    // Step 3: Additional operation
    err = workflow.ExecuteActivity(ctx, StepWithError, details).Get(ctx, nil)
    return err // If error, both compensations run in reverse order
}
```

**Java Implementation** (using Saga API):
```java
public class HelloSaga {
    @WorkflowInterface
    public interface GreetingWorkflow {
        @WorkflowMethod
        String getGreeting(String name);
    }

    public static class GreetingWorkflowImpl implements GreetingWorkflow {
        @Override
        public String getGreeting(String name) {
            // Create a Saga instance with compensation options
            Saga saga = new Saga(new Saga.Options.Builder()
                .setParallelCompensation(false) // Run compensations sequentially
                .build());
            
            try {
                // Step 1: Execute activity and register compensation
                String hello = Workflow.executeActivity(
                    activities::hello, 
                    String.class, 
                    name
                ).get();
                saga.addCompensation(activities::cleanupHello, name);
                
                // Step 2: Execute activity and register compensation
                String bye = Workflow.executeActivity(
                    activities::bye, 
                    String.class, 
                    name
                ).get();
                saga.addCompensation(activities::cleanupBye, name);
                
                // Step 3: This might fail
                Workflow.executeActivity(
                    activities::processFile, 
                    Void.class, 
                    name
                ).get();
                saga.addCompensation(activities::cleanupFile, name);
                
                return hello + "; " + bye;
                
            } catch (Exception e) {
                // On any error, run all registered compensations in reverse order
                saga.compensate();
                throw e;
            }
        }
    }
}
```

**Key Differences:**
- **Go**: Uses `defer` statements that execute in LIFO order when function returns
- **Java**: Uses explicit `Saga` object to track and trigger compensations
- **Both**: Compensations run in reverse order of registration
- **Both**: Compensations are idempotent and can handle partial failures

## Applicability
Use the Saga pattern when:
- You need to maintain consistency across multiple services or databases
- Traditional distributed transactions (2PC) are too slow or unavailable
- You can define compensating actions for each step in your business process
- Eventual consistency is acceptable for your use case
- You need to handle long-running transactions that may span hours or days

## Pros
- ✅ Maintains eventual consistency without distributed locks
- ✅ Each service can use its own database and transaction model
- ✅ Automatic compensation execution via `defer` ensures cleanup
- ✅ Scales better than two-phase commit protocols
- ✅ Temporal's durability guarantees compensations will execute even after worker failures

## Cons
- ❌ Eventual consistency only - intermediate states are visible to other processes
- ❌ Requires careful design of idempotent compensation activities
- ❌ More complex than simple ACID transactions
- ❌ Compensation logic must be maintained alongside forward logic
- ❌ Some operations may not have meaningful compensations

## Relations with Other Patterns
- Often combined with **Retry Policies** to handle transient failures before compensating
- Can use **Child Workflows** to organize complex sagas with multiple sub-sagas
- May leverage **Async Activity Completion** when compensations require external approval
- Works well with **Heartbeats** for long-running compensation activities
