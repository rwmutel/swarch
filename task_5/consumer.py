import hazelcast


if __name__ == "__main__":
    client = hazelcast.HazelcastClient(cluster_name="lab-2",
                                       cluster_members=["172.20.0.16:5701"])
    q = client.get_queue("bounded_q")
    elements = list()
    while True:
        element = q.take().result()
        elements.append(element)
        if element == 100:
            print("Consumer got poison pill (100) and shutting down",
                  flush=True)
            q.put(100).result()
            print(f"All popped elements: {elements}", flush=True)
            break
        print(f"Consumer got {element} from queue", flush=True)

    client.shutdown()
