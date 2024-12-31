using System;
using UnityEngine;

[Serializable]
public struct BoundsOffsetInt
{
	public Vector3Int offsetMin;
	public Vector3Int offsetMax;

	public BoundsOffsetInt (Vector3Int offsetMin, Vector3Int offsetMax)
	{
		this.offsetMin = offsetMin;
		this.offsetMax = offsetMax;
	}

	public BoundsInt Apply (BoundsInt bounds)
	{
		bounds.min += offsetMin;
		bounds.max += offsetMax;
		return bounds;
	}

	public BoundsOffset ToBoundsOffset ()
	{
		return new BoundsOffset(offsetMin, offsetMax);
	}
}