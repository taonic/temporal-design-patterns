// Stub class compiled at image-build time so the Temporal Java SDK and the
// Maven compiler plugin exercise their classloading paths once before any
// user code runs. The image factory copies this into src/main/java/, runs
// `mvn compile`, then deletes both the source and target/ from the snapshot.
//
// Living under _warmup/ keeps it out of the runtime source tree the runner
// uploads on each launch.

import io.temporal.activity.ActivityInterface;
import io.temporal.client.WorkflowClient;
import io.temporal.serviceclient.WorkflowServiceStubs;
import io.temporal.worker.WorkerFactory;
import io.temporal.workflow.WorkflowInterface;

public class Warmup {
    @SuppressWarnings("unused")
    private static final Class<?>[] FORCE_RESOLVE = {
        ActivityInterface.class,
        WorkflowInterface.class,
        WorkflowClient.class,
        WorkflowServiceStubs.class,
        WorkerFactory.class,
    };
}
