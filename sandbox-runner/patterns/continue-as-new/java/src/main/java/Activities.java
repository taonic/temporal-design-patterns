import io.temporal.activity.ActivityInterface;

import java.util.ArrayList;
import java.util.List;

@ActivityInterface
public interface Activities {
    List<String> fetchBatch(String cursor, int batchSize);

    void processRecord(String recordId);

    final class Impl implements Activities {
        @Override
        public List<String> fetchBatch(String cursor, int batchSize) {
            int start = cursor.isEmpty() ? 0 : Integer.parseInt(cursor) + 1;
            int end = Math.min(start + batchSize, Shared.TOTAL_RECORDS);
            List<String> out = new ArrayList<>();
            for (int i = start; i < end; i++) {
                out.add(String.valueOf(i));
            }
            return out;
        }

        @Override
        public void processRecord(String recordId) {
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
