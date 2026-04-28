import io.temporal.activity.ActivityOptions;
import io.temporal.workflow.Workflow;
import io.temporal.workflow.WorkflowInterface;
import io.temporal.workflow.WorkflowMethod;

import java.time.Duration;
import java.util.List;

@WorkflowInterface
public interface DataProcessorWorkflow {
    @WorkflowMethod
    int process(String cursor, int totalProcessed);

    final class Impl implements DataProcessorWorkflow {
        private final Activities activities = Workflow.newActivityStub(
                Activities.class,
                ActivityOptions.newBuilder()
                        .setStartToCloseTimeout(Duration.ofSeconds(10))
                        .build());

        @Override
        public int process(String cursor, int totalProcessed) {
            List<String> batch = activities.fetchBatch(cursor, Shared.BATCH_SIZE);

            for (String recordId : batch) {
                activities.processRecord(recordId);
                totalProcessed++;
                cursor = recordId;
            }

            Workflow.getLogger(DataProcessorWorkflow.class)
                    .info("Processed batch of {} (running total: {})", batch.size(), totalProcessed);

            if (batch.size() == Shared.BATCH_SIZE) {
                DataProcessorWorkflow next = Workflow.newContinueAsNewStub(DataProcessorWorkflow.class);
                next.process(cursor, totalProcessed);
            }

            return totalProcessed;
        }
    }
}
