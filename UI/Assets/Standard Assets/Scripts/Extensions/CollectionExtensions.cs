using System;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class CollectionExtensions 
	{
		public static List<T> ToList<T> (this T[] array)
		{
			return new List<T>(array);
		}

		public static T[] Add<T> (this T[] array, T element)
		{
			List<T> output = array.ToList();
			output.Add(element);
			return output.ToArray();
		}

		public static T[] Remove<T> (this T[] array, T element)
		{
			List<T> output = array.ToList();
			output.Remove(element);
			return output.ToArray();
		}

		public static T[] RemoveAt<T> (this T[] array, int index)
		{
			List<T> output = array.ToList();
			output.RemoveAt(index);
			return output.ToArray();
		}

		public static T[] AddRange<T> (this T[] array, IEnumerable<T> array2)
		{
			List<T> output = array.ToList();
			output.AddRange(array2);
			return output.ToArray();
		}

		public static bool Contains<T> (this T[] array, T element)
		{
			foreach (T obj in array)
			{
				if (obj == null)
				{
					if (element == null)
						return true;
				}
				else if (obj.Equals(element))
					return true;
			}
			return false;
		}

		public static int IndexOf<T> (this T[] array, T element)
		{
			for (int i = 0; i < array.Length; i ++)
			{
				if (array[i].Equals(element))
					return i;
			}
			return -1;
		}
		
		public static T[] Reverse<T> (this T[] array)
		{
			List<T> output = array.ToList();
			output.Reverse();
			return output.ToArray();
		}

		public static T[] AddArray<T> (this T[] array, Array array2)
		{
			List<T> output = array.ToList();
			for (int i = 0; i < array2.Length; i ++)
				output.Add((T) array2.GetValue(i));
			return output.ToArray();
		}

		public static string ToString<T> (this T[] array, string elementSeperator = ", ")
		{
            string output = "";
            foreach (T element in array)
                output += element.ToString() + elementSeperator;
			return output;
		}

		public static List<T> RemoveEach<T> (this List<T> array, IEnumerable<T> array2)
		{
			foreach (T element in array2)
				array.Remove(element);
			return array;
		}

		public static T[] Insert<T> (this T[] array, T element, int index)
		{
			List<T> output = array.ToList();
			output.Insert(index, element);
			return output.ToArray();
		}

		public static int IndexOf<T> (this Array array, T element)
		{
			for (int index = 0; index < array.GetLength(0); index ++)
			{
				if (((T) array.GetValue(index)).Equals(element))
				{
					return index;
				}
			}
			return -1;
		}

		public static T[] _Sort<T> (this T[] array, IComparer<T> sorter)
		{
			List<T> output = array.ToList();
			output.Sort(sorter);
			return output.ToArray();
		}

		public static int Count (this IEnumerable enumerable)
		{
			int output = 0;
			IEnumerator enumerator = enumerable.GetEnumerator();
			while (enumerator.MoveNext())
				output ++;
			return output;
		}

		public static T Get<T> (this IEnumerable<T> enumerable, int index)
		{
			IEnumerator enumerator = enumerable.GetEnumerator();
			while (enumerator.MoveNext())
			{
				index --;
				if (index < 0)
					return (T) enumerator.Current;
			}
			return default(T);
		}

		public static float GetMin (this float[] array)
		{
			float min = array[0];
			for (int i = 1; i < array.Length; i ++)
			{
				if (array[i] < min)
					min = array[i];
			}
			return min;
		}

		public static float GetMax (this float[] array)
		{
			float max = array[0];
			for (int i = 1; i < array.Length; i ++)
			{
				if (array[i] > max)
					max = array[i];
			}
			return max;
		}

		public static List<T> _Add<T> (this List<T> list, T element)
		{
			list.Add(element);
			return list;
		}
		
		public static int Length<T> (this List<T> list)
		{
			return list.Count;
		}
		
		public static List<T> _TrimEnd<T> (this List<T> list, int count)
		{
			list.RemoveRange(list.Count - count, count);
			return list;
		}
		
		public static List<T> _RemoveAt<T> (this List<T> list, int index)
		{
			list.RemoveAt(index);
			return list;
		}
		
		public static List<T> _Remove<T> (this List<T> list, T element)
		{
			list.Remove(element);
			return list;
		}
		
		public static T[] _RemoveAt<T> (this T[] array, int index)
		{
			array = array.RemoveAt(index);
			return array;
		}
		
		public static T[] _Remove<T> (this T[] array, T element)
		{
			array = array.Remove(element);
			return array;
		}
		
		public static T[] _Add<T> (this T[] array, T element)
		{
			array = array.Add(element);
			return array;
		}

		public static T1[] GetKeys<T1, T2> (this Dictionary<T1, T2> dict)
		{
			List<T1> output = new List<T1>();
			IEnumerator keyEnumerator = dict.Keys.GetEnumerator();
			while (keyEnumerator.MoveNext())
				output.Add((T1) keyEnumerator.Current);
			return output.ToArray();
		}

		public static void RotateRight (this IList list, int count)
		{
			object element = list[count - 1];
			list.RemoveAt(count - 1);
			list.Insert(0, element);
		}

		public static IEnumerable<IList> GetPermutations (this IList list, int count)
		{
			if (count == 1)
				yield return list;
			else
			{
				for (int i = 0; i < count; i ++)
				{
					foreach (IList permutation in GetPermutations(list, count - 1))
						yield return permutation;
					RotateRight (list, count);
				}
			}
		}

		public static IEnumerable<IList> GetPermutations (this IList list)
		{
			return list.GetPermutations(list.Count);
		}

		public static IEnumerable<IList> GetPermutations<T> (this T[] array, int count)
		{
			return array.ToList().GetPermutations(count);
		}

		public static IEnumerable<IList> GetPermutations<T> (this T[] array)
		{
			return array.ToList().GetPermutations(array.Length);
		}

		public static T[] GetHomogenized<T> (T element, uint count)
		{
			T[] output = new T[count];
			for (int i = 0; i < count; i ++)
				output[i] = element;
			return output;
		}
		
		public static List<T> TrimEnd<T> (this List<T> list, int count)
		{
			list.RemoveRange(list.Count - count, count);
			return list;
		}
	}
}