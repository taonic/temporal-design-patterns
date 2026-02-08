---
layout: default
title: Long Running Activity
parent: Long-Running and Operational Patterns
nav_order: 2
---

# Long Running Activity - Tracking Progress and Handling Cancellation with Heartbeats

## Overview

The Activity Heartbeat pattern enables long-running activities to report progress, handle cancellation gracefully, and resume from the last checkpoint after failures. Heartbeats inform Temporal that the activity is still alive and allow storing progress details that survive worker restarts.

## Problem

In long-running operations, you often need activities that:
- Process large datasets or perform time-consuming operations (minutes to hours)
- Report progress to avoid appearing stuck or timing out
- Resume from the last checkpoint after worker crashes or restarts
- Handle cancellation requests gracefully and clean up resources
- Avoid reprocessing already-completed work

Without heartbeats, you must:
- Set very long activity timeouts that delay failure detection
- Reprocess entire batches from the beginning on failures
- Have no visibility into activity progress
- Risk zombie activities that appear alive but are actually stuck
- Implement custom checkpointing and recovery logic

## Solution

Activity heartbeats use `Activity.getExecutionContext().heartbeat(details)` to periodically report progress. The heartbeat details are persisted and available to retry attempts, enabling resumption from the last checkpoint. Heartbeat timeouts detect stuck activities faster than execution timeouts.

## Implementation

### Basic Progress Tracking

```java
@ActivityInterface
public interface FileProcessingActivity {
  void processLargeFile(String filePath);
}

public class FileProcessingActivityImpl implements FileProcessingActivity {
  @Override
  public void processLargeFile(String filePath) {
    ActivityExecutionContext context = Activity.getExecutionContext();
    Optional<Integer> lastProcessedLine = context.getHeartbeatDetails(Integer.class);
    int startLine = lastProcessedLine.orElse(0);
    
    try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
      // Skip already processed lines
      for (int i = 0; i < startLine; i++) {
        reader.readLine();
      }
      
      String line;
      int currentLine = startLine;
      while ((line = reader.readLine()) != null) {
        processLine(line);
        currentLine++;
        
        // Heartbeat every 100 lines
        if (currentLine % 100 == 0) {
          context.heartbeat(currentLine);
        }
      }
    }
  }
}
```

### Handling Cancellation

```java
public class FileProcessingActivityImpl implements FileProcessingActivity {
  @Override
  public void processLargeFile(String filePath) {
    ActivityExecutionContext context = Activity.getExecutionContext();
    Optional<Integer> lastProcessedLine = context.getHeartbeatDetails(Integer.class);
    int currentLine = lastProcessedLine.orElse(0);
    
    try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
      for (int i = 0; i < currentLine; i++) {
        reader.readLine();
      }
      
      String line;
      while ((line = reader.readLine()) != null) {
        // Check for cancellation
        context.heartbeat(currentLine);
        
        try {
          processLine(line);
          currentLine++;
        } catch (ActivityCancelledException e) {
          // Cleanup before cancellation
          cleanupResources();
          throw e;
        }
      }
    }
  }
}
```

### Advanced: Complex Progress State

```java
public class BatchProcessingActivityImpl implements BatchProcessingActivity {
  
  static class ProgressState {
    int processedCount;
    int failedCount;
    String lastProcessedId;
    
    // Constructor, getters, setters
  }
  
  @Override
  public BatchResult processBatch(List<String> itemIds) {
    ActivityExecutionContext context = Activity.getExecutionContext();
    Optional<ProgressState> details = context.getHeartbeatDetails(ProgressState.class);
    ProgressState progress = details.orElse(new ProgressState());
    
    // Resume from last checkpoint
    int startIndex = itemIds.indexOf(progress.lastProcessedId) + 1;
    
    for (int i = startIndex; i < itemIds.size(); i++) {
      String itemId = itemIds.get(i);
      
      try {
        processItem(itemId);
        progress.processedCount++;
      } catch (Exception e) {
        progress.failedCount++;
      }
      
      progress.lastProcessedId = itemId;
      context.heartbeat(progress);
    }
    
    return new BatchResult(progress.processedCount, progress.failedCount);
  }
}
```

## Key Components

1. **ActivityExecutionContext**: Provides access to heartbeat functionality
2. **heartbeat(details)**: Reports progress and stores checkpoint data
3. **getHeartbeatDetails()**: Retrieves progress from previous attempt on retry
4. **Heartbeat Timeout**: Configured in ActivityOptions, triggers retry if exceeded
5. **ActivityCancelledException**: Thrown when activity is cancelled, enabling cleanup

## When to Use

**Ideal for:**
- Batch processing of large datasets
- File uploads/downloads with progress tracking
- Database migrations or bulk operations
- Long-running computations (ML training, video encoding)
- External API polling with multiple attempts
- Any activity running longer than 30 seconds

**Not ideal for:**
- Quick operations (< 10 seconds)
- Operations that can't be checkpointed
- Activities requiring exact-once semantics without idempotency
- Real-time streaming (use workflows instead)

## Benefits

- **Fault Tolerance**: Resume from last checkpoint after failures
- **Fast Failure Detection**: Heartbeat timeout detects stuck activities quickly
- **Progress Visibility**: Monitor activity progress in real-time
- **Graceful Cancellation**: Clean up resources before terminating
- **Resource Efficiency**: Avoid reprocessing completed work
- **Worker Mobility**: Activities can move between workers seamlessly

## Trade-offs

- **Network Overhead**: Frequent heartbeats increase network traffic
- **Complexity**: Requires checkpointing logic and state management
- **Idempotency**: Must handle partial reprocessing of last checkpoint
- **Heartbeat Frequency**: Balance between responsiveness and overhead
- **State Size**: Heartbeat details have size limits (avoid large objects)

## How It Works

1. Activity starts and checks `getHeartbeatDetails()` for previous progress
2. Activity resumes from last checkpoint (or starts from beginning)
3. Activity processes work and periodically calls `heartbeat(progress)`
4. Temporal records heartbeat timestamp and details
5. If worker crashes:
   - Heartbeat timeout expires
   - Activity is retried on another worker
   - New attempt retrieves details and resumes
6. If workflow cancels activity:
   - Next heartbeat throws `ActivityCancelledException`
   - Activity performs cleanup and exits

## Comparison with Alternatives

| Approach | Progress Tracking | Resumable | Cancellation | Complexity |
|----------|------------------|-----------|--------------|------------|
| Heartbeat | Yes | Yes | Graceful | Medium |
| Long Timeout | No | No | Delayed | Low |
| Child Workflows | Yes | Yes | Immediate | High |
| Local Activity | No | No | N/A | Low |

## Related Patterns

- **Batch Processing**: Processing large datasets with checkpointing
- **Saga Pattern**: Compensating transactions with long-running steps
- **Activity Retry**: Automatic retry with exponential backoff
- **Cancellation Scopes**: Workflow-level cancellation handling

## Sample Code

- [Heartbeating Activity Batch](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/batch/heartbeatingactivity) - Complete batch processing implementation
- [Auto-Heartbeating](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/autoheartbeat) - Automatic heartbeating via interceptor

## Best Practices

1. **Set Heartbeat Timeout**: Configure to 2-3x expected heartbeat interval
2. **Heartbeat Frequency**: Balance between responsiveness (every 10-30s) and overhead
3. **Checkpoint Strategically**: Save progress at meaningful boundaries (records, pages, chunks)
4. **Keep Details Small**: Store minimal state (IDs, offsets, counts), not full objects
5. **Handle Idempotency**: Ensure reprocessing last checkpoint is safe
6. **Check Cancellation**: Heartbeat regularly to detect cancellation quickly
7. **Cleanup on Cancel**: Use try-catch to handle `ActivityCancelledException`
8. **Log Progress**: Log heartbeat details for debugging and monitoring
9. **Test Resumption**: Verify activities resume correctly after simulated failures
10. **Avoid Heartbeat Spam**: Don't heartbeat on every iteration of tight loops
