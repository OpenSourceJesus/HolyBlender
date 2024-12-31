using System;
using UnityEngine;
using System.Collections.Generic;

[Serializable]
public class SerializableDictionary<T1, T2> : Dictionary<T1, T2>
{
	public List<T1> keys = new List<T1>();
	public List<T2> values = new List<T2>();
	
	
	public T2 this[T1 key]
	{
		get
		{
			return base[key];
		}
		set
		{
			int index = keys.IndexOf(key);
			if (index == -1)
				Add (key, value);
			else
				values[index] = value;
		}
	}
	public void Init ()
	{
		base.Clear();
		for (int i = 0; i < keys.Count; i ++)
			base.Add(keys[i], values[i]);
	}

	public new void Add (T1 key, T2 value)
	{
		base.Add(key, value);
		keys.Add(key);
		values.Add(value);
	}

	public new bool Remove (T1 key)
	{
		T2 value;
		if (TryGetValue(key, out value) && base.Remove(key))
		{
			keys.Remove(key);
			values.Remove(value);
			return true;
		}
		else
			return false;
	}

	public new void Clear (T1 key)
	{
		base.Clear();
		keys.Clear();
		values.Clear();
	}
}