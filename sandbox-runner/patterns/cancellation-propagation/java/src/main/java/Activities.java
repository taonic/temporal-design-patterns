import io.temporal.activity.Activity;
import io.temporal.activity.ActivityInterface;
import io.temporal.client.ActivityCanceledException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@ActivityInterface
public interface Activities {
    void applyStep(String orderId, String step);

    void holdReservation(String orderId, String step);

    void compensateStep(String orderId, String step);

    final class Impl implements Activities {
        private static final Logger log = LoggerFactory.getLogger(Activities.class);

        @Override
        public void applyStep(String orderId, String step) {
            // Reserve a resource for one fulfillment step.
            log.info("Applied {} for order {}", step, orderId);
            sleep(100);
        }

        @Override
        public void holdReservation(String orderId, String step) {
            // Long-running activity that keeps the reservation open until it is
            // cancelled. It heartbeats on each iteration so the server can
            // deliver the cancellation request.
            log.info("Holding {} for order {}", step, orderId);
            try {
                while (true) {
                    sleep(1000);
                    // heartbeat throws ActivityCanceledException once cancellation
                    // has been requested for this activity.
                    Activity.getExecutionContext().heartbeat(step);
                }
            } catch (ActivityCanceledException e) {
                log.info("Reservation for {} released on cancellation", step, orderId);
                throw e;
            }
        }

        @Override
        public void compensateStep(String orderId, String step) {
            // Undo a previously applied fulfillment step.
            log.info("Compensated {} for order {}", step, orderId);
            sleep(100);
        }

        private void sleep(long millis) {
            try {
                Thread.sleep(millis);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
