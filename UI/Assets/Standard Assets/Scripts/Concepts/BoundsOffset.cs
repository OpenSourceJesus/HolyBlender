using System;
using UnityEngine;

[Serializable]
public struct BoundsOffset
{
	public Vector3 offsetMin;
	public Vector3 offsetMax;

	public BoundsOffset (Vector3 offsetMin, Vector3 offsetMax)
	{
		this.offsetMin = offsetMin;
		this.offsetMax = offsetMax;
	}

	public Bounds Apply (Bounds bounds)
	{
		bounds.min += offsetMin;
		bounds.max += offsetMax;
		return bounds;
	}
}