#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;
using System.Collections.Generic;

namespace Extensions
{
	public class SelectionExtensions
	{
		public static T[] GetSelected<T> () where T : Object
		{
			List<T> output = new List<T>();
			foreach (Transform trs in Selection.transforms)
			{
				T obj = trs.GetComponent<T>();
				if (obj != null)
					output.Add(obj);
			}
			return output.ToArray();
		}
	}
}
#endif