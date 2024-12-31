using System;
using Extensions;
using UnityEngine;

[Serializable]
public class Zone2D : Shape2D
{
	public Collider2D collider;
	public Transform[] transforms = new Transform[0];
	public Type type;

	public Zone2D ()
	{
	}

	public void SetCornersAndEdges (Shape2D shape)
	{
		corners = shape.corners;
		edges = shape.edges;
	}

	public static Zone2D Make (Transform[] transforms)
	{
		Zone2D output = new Zone2D();
		output.type = Type.Transforms;
		output.transforms = transforms;
		output.corners = new Vector2[transforms.Length];
		for (int i = 0; i < transforms.Length; i ++)
		{
			Transform trs = transforms[i];
			output.corners[i] = trs.position;
		}
        output.SetEdges_Polygon ();
		return output;
	}

	public static Zone2D Make (Collider2D collider)
	{
		Zone2D output = new Zone2D();
		output.type = Type.ColliderPoints;
		output.collider = collider;
		EdgeCollider2D edgeCollider = collider as EdgeCollider2D;
		if (edgeCollider != null)
			output.corners = edgeCollider.points;
		else
		{
			PolygonCollider2D polygonCollider = collider as PolygonCollider2D;
			if (polygonCollider != null)
				output.corners = polygonCollider.points;
		}
		output.SetEdges_Polygon ();
		return output;
	}

	public Zone2D Make ()
	{
		if (type == Type.ColliderPoints)
			return Make(collider);
		else// if (type == Type.Transforms)
			return Make(transforms);
	}

	public enum Type
	{
		ColliderPoints,
		Transforms
	}
}