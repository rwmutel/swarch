import hazelcast


if __name__ == "__main__":
    print("Launched Client!")
    KEY = "key"
    client = hazelcast.HazelcastClient(cluster_name="lab-2", cluster_members=["172.20.0.16:5701"])
    print("Client connected to cluster")
    map = client.get_map("dist-map-no-lock").blocking()
    print("Client got the map and starts incrementing")
    map.put_if_absent(KEY, 0)

    i = 0
    while i < 10000:
        if i % 1000 == 1:
            print(f"Client incremented the value {i} times")
        old_value = map.get_entry_view(KEY).value
        if map.replace_if_same(KEY, old_value, old_value + 1):
            i += 1

    client.shutdown()
