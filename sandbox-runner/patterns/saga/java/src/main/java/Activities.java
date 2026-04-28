import io.temporal.activity.ActivityInterface;

@ActivityInterface
public interface Activities {
    void withdraw(Shared.TransferDetails details);

    void deposit(Shared.TransferDetails details);

    void notifyDownstream(Shared.TransferDetails details);

    void withdrawCompensation(Shared.TransferDetails details);

    void depositCompensation(Shared.TransferDetails details);

    final class Impl implements Activities {
        @Override
        public void withdraw(Shared.TransferDetails details) {
            System.out.printf("Withdrew $%d from %s%n", details.amount(), details.fromAccount());
        }

        @Override
        public void deposit(Shared.TransferDetails details) {
            System.out.printf("Deposited $%d to %s%n", details.amount(), details.toAccount());
        }

        @Override
        public void notifyDownstream(Shared.TransferDetails details) {
            System.out.printf(
                    "Notify: simulating downstream failure for transfer %s%n",
                    details.transferId());
            // Comment out the throw to watch the saga succeed end-to-end:
            throw new RuntimeException("notification service down");
        }

        @Override
        public void withdrawCompensation(Shared.TransferDetails details) {
            System.out.printf("Refunded $%d to %s%n", details.amount(), details.fromAccount());
        }

        @Override
        public void depositCompensation(Shared.TransferDetails details) {
            System.out.printf(
                    "Reversed deposit of $%d from %s%n", details.amount(), details.toAccount());
        }
    }
}
