Title: Reusing Deleted Slots in the Simple GPU Hash Table
Date: 2020-03-06 15:00
Tags: Programming
Category: Blog
Slug: ReusingDeletedSlot
Author: David Farrell
Summary: Reusing the deleted slots in the simple GPU hash table
Status: draft

# Reusing Deleted Slots

If the lock free hash table is used for long enough with many inserts and deletes, then it will fill up with keys that have been marked for deletion. Because the table never moves keys around (even deleted keys), this causes the table to fill up with garbage keys, which causes the table's performance to grow worse over time.

To help with this problem, we can reuse deleted slots. This requires that we change the contract of the lock free hash table so that inserts and deletes are not allowed to happen at the same time. Then, the delete function can mark keys (not values) as tombstoned. The insert function will then place keys into either empty or tombstoned slots. Tombstones are a special sentinal value separate from the empty sentinel which mark keys as deleted, but still in the hash table so that lookups still work.

This works as long as inserts and deletes do not happen in parallel, and never at the same time. However, lookups can happen concurrently with both inserts and deletes with this modification.

Note that this means keys get moved around; a key is assigned a slot, but when it's deleted and then re-inserted, it can be assigned a different slot.

The possible states of key/values during inserts are then:

+ empty/empty
+ key/empty
+ empty/value
+ key/value
+ tombstone/empty

Once all the writes from the insertion kernel have finished, then the possible states for a key are empty/empty, key/value, or tombstone/empty.

So then the possible states for a key/value pair during deletes are then:

+ empty/empty
+ key/value
+ key/empty
+ tombstone/value
+ tombstone/empty

And once all the writes from the deletion kernel have finished, the possible states for a key are empty/empty, key/value, or tombstone/empty.

The code for insert and delete becomes:

```cpp
void gpu_hashtable_insert(KeyValue* hashtable, uint32_t key, uint32_t value)
{
    uint32_t slot = hash(key);

    while (true)
    {
        uint32_t prev = atomicCAS(&hashtable[slot].key, kEmpty, key);
        if (prev == kEmpty || prev == key)
        {
            hashtable[slot].value = value;
            break;
        }
        if (prev == kTombstone)
        {
            prev = atomicCAS(&hashtable[slot].key, kTombstone, key);
            if (prev == kTombstone)
            {
                hashtable[slot].value = value;
                break;
            }
        }
        slot = (slot + 1) & (kHashTableCapacity-1);
    }
}

void gpu_hashtable_delete(KeyValue* hashtable, uint32_t key, uint32_t value)
{
    uint32_t slot = hash(key);

    while (true)
    {
        if (hashtable[slot].key == key)
        {
            hashtable[slot].key = kTombstone;
            hashtable[slot].value = kEmpty;
            return;
        }
        if (hashtable[slot].key == kEmpty)
        {
            return;
        }
        slot = (slot + 1) & (kHashTableCapacity - 1);
    }
}
```

The example code doesn't use this variant because I wanted to show a generic implementation that supports concurrent inserts, lookups, and deletes.

