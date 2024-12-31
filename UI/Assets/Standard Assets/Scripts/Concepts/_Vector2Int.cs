using System;
using UnityEngine;

[Serializable]
public struct _Vector2Int
{
	public int x;
	public int y;

	public _Vector2Int (int x, int y)
	{
		this.x = x;
		this.y = y;
	}

	public Vector2Int ToVec2Int ()
	{
		return new Vector2Int(x, y);
	}

	public static _Vector2Int FromVec2Int (Vector2Int v)
	{
		return new _Vector2Int(v.x, v.y);
	}
}