using UnityEngine;
using Extensions;
using System.Collections.Generic;

public class SerializableFloatIndexedDictionary<T> : SerializableDictionary<float, T>
{
	public KeyValuePair<int, T> this[float index]
	{
		get
		{
			int actualIndex = MathfExtensions.GetIndexOfClosestNumber(index, keys.ToArray());
			return new KeyValuePair<int, T>(actualIndex, values[actualIndex]);
		}
		set
		{
			int actualIndex = MathfExtensions.GetIndexOfClosestNumber(index, keys.ToArray());
			base[keys[actualIndex]] = value.Value;
		}
	}
}