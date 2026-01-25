# Request-Response via Updates

## Overview

Workflow Updates enable synchronous request-response interactions where clients receive immediate, typed responses while the workflow continues processing. Updates modify workflow state, validate inputs, and return results directly to the caller with strong consistency guarantees.

## Problem

In distributed systems, you often need workflows that:
- Must provide immediate feedback to clients (validation results, confirmation IDs)
- Require strong consistency guarantees for operations
- Need typed error handling for validation failures
- Should validate inputs before accepting work
- Allow external systems to modify workflow state synchronously

Without Updates, clients must:
- Use signals and poll via queries (complex, eventually consistent)
- Wait for entire workflow completion (slow)
- Implement complex coordination logic
- Handle race conditions between signals and queries

## Solution

Temporal's Update API executes an update handler that can validate inputs, modify state, and return values synchronously. The update is recorded in workflow history before returning, providing strong consistency.

## Implementation

### Basic Update

```java
public class OrderManager {
  public OrderStatus addOrder(String workflowId, OrderRequest request) {
    OrderWorkflow workflow = 
        client.newWorkflowStub(OrderWorkflow.class, workflowId);
    
    // Execute update and get synchronous response
    OrderStatus status = workflow.addOrder(request);
    
    // Client receives status immediately
    return status;
  }
}

@WorkflowInterface
public interface OrderWorkflow {
  @WorkflowMethod
  void processOrders();
  
  @UpdateMethod
  OrderStatus addOrder(OrderRequest request);
  
  @QueryMethod
  List<Order> getOrders();
}

public class OrderWorkflowImpl implements OrderWorkflow {
  private Map<String, Order> orders = new HashMap<>();
  
  @Override
  public void processOrders() {
    Workflow.await(() -> false); // Run forever
  }
  
  @Override
  public OrderStatus addOrder(OrderRequest request) {
    // Validate inputs
    if (request.getAmount() <= 0) {
      throw new IllegalArgumentException("Amount must be positive");
    }
    
    if (orders.size() >= MAX_ORDERS) {
      throw new IllegalStateException("Order limit reached");
    }
    
    // Modify state
    String orderId = generateOrderId();
    orders.put(orderId, new Order(orderId, request));
    
    // Return immediately
    return new OrderStatus(orderId, "ACCEPTED");
  }
  
  @Override
  public List<Order> getOrders() {
    return new ArrayList<>(orders.values());
  }
}
```

### Update with Validation

```java
public class AccountWorkflowImpl implements AccountWorkflow {
  private BigDecimal balance = BigDecimal.ZERO;
  private List<Transaction> transactions = new ArrayList<>();
  
  @Override
  public TransactionResult deposit(BigDecimal amount) {
    // Validate
    if (amount.compareTo(BigDecimal.ZERO) <= 0) {
      throw new IllegalArgumentException("Deposit amount must be positive");
    }
    
    // Update state
    balance = balance.add(amount);
    String txId = UUID.randomUUID().toString();
    transactions.add(new Transaction(txId, "DEPOSIT", amount));
    
    // Return result
    return new TransactionResult(txId, balance);
  }
  
  @Override
  public TransactionResult withdraw(BigDecimal amount) {
    // Validate
    if (amount.compareTo(BigDecimal.ZERO) <= 0) {
      throw new IllegalArgumentException("Withdrawal amount must be positive");
    }
    
    if (balance.compareTo(amount) < 0) {
      throw new IllegalStateException("Insufficient funds");
    }
    
    // Update state
    balance = balance.subtract(amount);
    String txId = UUID.randomUUID().toString();
    transactions.add(new Transaction(txId, "WITHDRAWAL", amount));
    
    // Return result
    return new TransactionResult(txId, balance);
  }
}
```

## Key Components

1. **Update Handler**: Method annotated with @UpdateMethod that modifies state and returns synchronously
2. **Validation Logic**: Input validation that throws typed exceptions
3. **State Modification**: Updates to workflow state variables
4. **Typed Return**: Synchronous return value sent to client
5. **Strong Consistency**: Update recorded in history before returning

## When to Use

**Ideal for:**
- Request-response patterns requiring immediate confirmation
- Input validation before accepting work
- Synchronous state modifications with typed responses
- Operations requiring strong consistency guarantees
- Entity workflows that need external state updates

**Not ideal for:**
- Fire-and-forget operations (use Signals)
- Read-only operations (use Queries)
- High-throughput scenarios where latency matters (updates are slower than signals)
- Operations that don't need immediate response

## Benefits

- **Synchronous Response**: Client receives typed return value immediately
- **Typed Errors**: Validation failures return as typed exceptions
- **Strong Consistency**: Update is recorded in history before returning
- **State Modification**: Directly modify workflow state from external systems
- **Validation**: Reject invalid inputs before accepting work

## Trade-offs

- **Higher Latency**: Updates are slower than signals (requires history write)
- **Blocking**: Update handler blocks workflow task execution
- **Resource Usage**: Update handlers consume workflow task execution time
- **Complexity**: More complex than signals for simple notifications

## Comparison with Alternatives

| Approach | Use Case | Response Type | Latency | Consistency |
|----------|----------|---------------|---------|-------------|
| Update | Request-response | Sync typed value | Higher | Strong |
| Signal | Fire-and-forget | None | Lower | Eventual |
| Query | Read-only | Sync typed value | Lowest | Eventual |

## Related Patterns

- **Signal**: Fire-and-forget state modifications
- **Query**: Read-only state inspection
- **Entity Workflow**: Long-running workflows representing business entities
- **[Early Return](early-return.md)**: Returning intermediate results before workflow completion

## Best Practices

1. **Validate Early**: Check inputs at the start of update handler to fail fast
2. **Handle Errors**: Throw typed exceptions for validation failures
3. **Return Quickly**: Don't perform long operations in update handler
4. **Idempotency**: Track processed update IDs if updates can be retried
5. **Timeout Configuration**: Set appropriate update timeouts
6. **State Consistency**: Ensure state modifications are atomic within the handler

## Comparison: Signal vs Update

**Use Signal when:**
- No immediate response needed
- Fire-and-forget semantics acceptable
- Minimizing latency is critical
- Eventually consistent is acceptable

**Use Update when:**
- Client needs immediate confirmation
- Typed return values required
- Input validation before acceptance
- Strong consistency guarantees needed
