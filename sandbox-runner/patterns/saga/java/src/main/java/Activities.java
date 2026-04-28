import io.temporal.activity.ActivityInterface;

@ActivityInterface
public interface Activities {
    void createAccount(Shared.OpenAccountRequest req);

    void addAddress(Shared.OpenAccountRequest req);

    void addClient(Shared.OpenAccountRequest req);

    void addBankAccount(Shared.OpenAccountRequest req);

    void clearPostalAddresses(Shared.OpenAccountRequest req);

    void removeClient(Shared.OpenAccountRequest req);

    void disconnectBankAccounts(Shared.OpenAccountRequest req);

    final class Impl implements Activities {
        @Override
        public void createAccount(Shared.OpenAccountRequest req) {
            System.out.printf("Created account %s for %s%n", req.accountId(), req.clientName());
        }

        @Override
        public void addAddress(Shared.OpenAccountRequest req) {
            System.out.printf("Added address '%s' to %s%n", req.address(), req.accountId());
        }

        @Override
        public void addClient(Shared.OpenAccountRequest req) {
            System.out.printf("Added client %s to %s%n", req.clientEmail(), req.accountId());
        }

        @Override
        public void addBankAccount(Shared.OpenAccountRequest req) {
            System.out.printf(
                    "Linking bank account %s: simulating downstream failure%n",
                    req.bankAccount());
            // Comment out the throw to watch the saga succeed end-to-end:
            throw new RuntimeException("bank link service down");
        }

        @Override
        public void clearPostalAddresses(Shared.OpenAccountRequest req) {
            System.out.printf("Cleared postal addresses for %s%n", req.accountId());
        }

        @Override
        public void removeClient(Shared.OpenAccountRequest req) {
            System.out.printf("Removed client from %s%n", req.accountId());
        }

        @Override
        public void disconnectBankAccounts(Shared.OpenAccountRequest req) {
            System.out.printf("Disconnected any bank accounts from %s%n", req.accountId());
        }
    }
}
