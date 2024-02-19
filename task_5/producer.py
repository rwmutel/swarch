import hazelcast


if __name__ == "__main__":
    print("Launched Producer")
    client = hazelcast.HazelcastClient(cluster_name="lab-2",
                                       cluster_members=["172.20.0.16:5701"])
    print("Producer got client")
    q = client.get_queue("bounded_q")
    print("Producer got the queue")
    for i in range(100):
        q.put(i).result()
        print(f"Producer put {i} in queue", flush=True)

    q.put(100).result()
    print("Stopping by putting 100 in queue", flush=True)

    client.shutdown()
