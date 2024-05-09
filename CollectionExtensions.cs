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
}