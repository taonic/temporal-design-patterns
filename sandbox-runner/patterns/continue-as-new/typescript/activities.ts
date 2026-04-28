import { TOTAL_RECORDS } from "./shared";

export interface DataRecord {
  id: string;
}

export async function fetchBatch(cursor: string, batchSize: number): Promise<DataRecord[]> {
  const start = cursor === "" ? 0 : Number.parseInt(cursor, 10) + 1;
  const end = Math.min(start + batchSize, TOTAL_RECORDS);
  const batch: DataRecord[] = [];
  for (let i = start; i < end; i++) {
    batch.push({ id: String(i) });
  }
  return batch;
}

export async function processRecord(record: DataRecord): Promise<void> {
  await new Promise((r) => setTimeout(r, 50));
}
