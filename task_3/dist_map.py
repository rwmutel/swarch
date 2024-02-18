import hazelcast
from hazelcast import future
from tqdm import tqdm


if __name__ == "__main__":
    client = hazelcast.HazelcastClient(cluster_name="lab-2")
    map = client.get_map("dist-map")
    f = future.combine_futures(
        [map.put(f"Key {i:3}", i) for i in tqdm(range(1000))])

    assert all([i is None for i in f.result()])

    client.shutdown()
