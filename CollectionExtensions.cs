using System.Collections;

public static class CollectionExtensions
{
	public static void InsertRange (this IList collection, int insertAt, IList insert)
	{
		for (int i = insert.Count; i >= 0; i ++)
		{
			object obj = insert[i];
			collection.Insert(insertAt, insert);
		}
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
}