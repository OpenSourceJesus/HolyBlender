using System;
using Extensions;
using UnityEngine;

[Serializable]
public class Rect2D : Shape2D
{
	public Vector2 center;
	public Vector2 size;
	public float rotation;

	public Rect2D (Vector2 center, Vector2 size, float rotation)
	{
		this.center = center;
		this.size = size;
		this.rotation = rotation;
		SetCornersAndEdges ();
	}

	public void SetCornersAndEdges ()
	{
		corners = new Vector2[4];
		corners[0] = (center - size / 2).Rotate(center, rotation);
		corners[1] = (center + new Vector2(-size.x, size.y) / 2).Rotate(center, rotation);
		corners[2] = (center + size / 2).Rotate(center, rotation);
		corners[3] = (center + new Vector2(size.x, -size.y) / 2).Rotate(center, rotation);
		SetEdges_Polygon ();
	}

	public void SetCenter (Vector2 center)
	{
		this.center = center;
		SetCornersAndEdges ();
	}

	public void SetSize (Vector2 size)
	{
		this.size = size;
		SetCornersAndEdges ();
	}

	public void SetRotation (float rotation)
	{
		this.rotation = rotation;
		SetCornersAndEdges ();
	}
}