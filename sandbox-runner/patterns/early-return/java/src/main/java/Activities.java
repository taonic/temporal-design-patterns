import io.temporal.activity.ActivityInterface;

@ActivityInterface
public interface Activities {
    Shared.Transaction initTransaction(Shared.TransactionRequest req);

    void completeTransaction(Shared.Transaction tx);

    void cancelTransaction(Shared.Transaction tx);

    final class Impl implements Activities {
        @Override
        public Shared.Transaction initTransaction(Shared.TransactionRequest req) {
            System.out.printf("Init: validating %.2f %s%n", req.amount(), req.currency());
            if (req.amount() <= 0) {
                throw new RuntimeException("Invalid amount: " + req.amount());
            }
            return new Shared.Transaction("tx-" + System.currentTimeMillis(), "initialized");
        }

        @Override
        public void completeTransaction(Shared.Transaction tx) {
            // Simulate slow background settlement so the early-return effect is visible.
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.printf("Completed transaction %s%n", tx.id());
        }

        @Override
        public void cancelTransaction(Shared.Transaction tx) {
            String id = tx == null ? "(uninitialized)" : tx.id();
            System.out.printf("Cancelled transaction %s%n", id);
        }
    }
}
