import hazelcast


if __name__ == "__main__":
    print("Launched Client!")
    KEY = "key"
    client = hazelcast.HazelcastClient(cluster_name="lab-2", cluster_members=["172.20.0.16:5701"])
    print("Client connected to cluster")
    map = client.get_map("dist-map-no-lock").blocking()
    print("Client got the map and starts incrementing")
    if not map.contains_key(KEY):
        map.put(KEY, 0)

    for i in range(10000):
        if i % 1000 == 1:
            print(f"Client incremented the value {i} times (pessimistic lock)")
        map.put(KEY, map.get_entry_view(KEY).value + 1)

    client.shutdown()
