using System;
using UnityEngine;
using Random = UnityEngine.Random;

[Serializable]
public class Shape3D
{
	public Vector3[] corners;
	public LineSegment3D[] edges;

	public Shape3D (Vector3[] corners)
	{
		this.corners = corners;
		SetEdges ();
	}

	public Shape3D (LineSegment3D[] edges)
	{
		this.edges = edges;
		SetCorners ();
	}

	public virtual void SetCorners ()
	{
		corners = new Vector3[edges.Length];
		for (int i = 0; i < edges.Length; i ++)
			corners[i] = edges[i].end;
	}

	public virtual void SetEdges ()
	{
		edges = new LineSegment3D[corners.Length];
		Vector3 previousCorner = corners[corners.Length - 1];
		for (int i = 0; i < corners.Length; i ++)
		{
			Vector3 corner = corners[i];
			edges[i] = new LineSegment3D(previousCorner, corner);
			previousCorner = corner;
		}
	}

	public virtual float GetPerimeter ()
	{
		float output = 0;
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment3D edge = edges[i];
			output += edge.GetLength();
		}
		return output;
	}

	public virtual Vector3 GetPointOnPerimeter (float distance)
	{
		float perimeter = GetPerimeter();
		while (true)
		{
			for (int i = 0; i < edges.Length; i ++)
			{
				LineSegment3D edge = edges[i];
				float edgeLength = edge.GetLength();
				distance -= edgeLength;
				if (distance <= 0)
					return edge.GetPointWithDirectedDistance(edgeLength + distance);
			}
		}
	}

	public virtual bool Contains (Vector3 point, bool shouldIncludeEndPoints = true, float checkDistance = 99999)
	{
		LineSegment3D checkLineSegment = new LineSegment3D(point, point + (Random.onUnitSphere.normalized * Random.value * checkDistance));
		int collisionCount = 0;
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment3D edge = edges[i];
			if (edge.DoIIntersectWithLineSegment(checkLineSegment, shouldIncludeEndPoints))
				collisionCount ++;
		}
		return collisionCount % 2 == 1;
	}

	public virtual Vector3 GetRandomPoint (bool checkIfContained = false)
	{
		float perimeter = GetPerimeter();
		do
		{
			Vector3 point1 = GetPointOnPerimeter(Random.Range(0, perimeter));
			Vector3 point2 = GetPointOnPerimeter(Random.Range(0, perimeter));
			Vector3 output = (point1 + point2) / 2;
			if (Contains(output))
				return output;
		} while (true);
	}
}