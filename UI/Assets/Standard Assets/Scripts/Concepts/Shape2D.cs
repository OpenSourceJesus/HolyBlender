using System;
using UnityEngine;
using System.Collections.Generic;
using Random = UnityEngine.Random;

[Serializable]
public class Shape2D
{
	public Vector2[] corners = new Vector2[0];
	public LineSegment2D[] edges = new LineSegment2D[0];

	public Shape2D ()
	{
	}

	public Shape2D (params Vector2[] corners)
	{
		this.corners = corners;
		SetEdges_Polygon ();
	}

	public Shape2D (params LineSegment2D[] edges)
	{
		this.edges = edges;
		SetCorners_Polygon ();
	}

#if UNITY_EDITOR
	public virtual void DrawGizmos (Color color)
	{
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			edge.DrawGizmos (color);
		}
	}
#endif

	public virtual void SetCorners_Polygon ()
	{
		corners = new Vector2[edges.Length];
		for (int i = 0; i < edges.Length; i ++)
			corners[i] = edges[i].end;
	}

	public virtual void SetEdges_Polygon ()
	{
		edges = new LineSegment2D[corners.Length];
		Vector3 previousCorner = corners[corners.Length - 1];
		for (int i = 0; i < corners.Length; i ++)
		{
			Vector2 corner = corners[i];
			edges[i] = new LineSegment2D(previousCorner, corner);
			previousCorner = corner;
		}
	}

	public virtual float GetPerimeter ()
	{
		float output = 0;
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			output += edge.GetLength();
		}
		return output;
	}

	public virtual Vector2 GetPointOnPerimeter (float distance)
	{
		float perimeter = GetPerimeter();
		while (true)
		{
			for (int i = 0; i < edges.Length; i ++)
			{
				LineSegment2D edge = edges[i];
				float edgeLength = edge.GetLength();
				distance -= edgeLength;
				if (distance <= 0)
					return edge.GetPointWithDirectedDistance(edgeLength + distance);
			}
		}
	}

	public virtual bool Contains_Polygon (Vector2 point, bool equalPointsIntersect = true, float checkDistance = 99999)
	{
		LineSegment2D checkLineSegment = new LineSegment2D(point, point + (Random.insideUnitCircle.normalized * checkDistance));
		int collisionCount = 0;
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			if (edge.DoIIntersectWithLineSegment(checkLineSegment, equalPointsIntersect))
				collisionCount ++;
		}
		return collisionCount % 2 == 1;
	}

	public virtual bool IsPolygon ()
	{
		throw new NotImplementedException();
	}

	public virtual bool DoIIntersectWithLineSegment (LineSegment2D lineSegment, bool equalPointsIntersect = true)
	{
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			if (edge.DoIIntersectWithLineSegment(lineSegment, equalPointsIntersect))
				return true;
		}
		return false;
	}

	public virtual Vector2 GetRandomPoint (bool checkIfContained = true, bool containsEdges = true, float checkDistance = 99999)
	{
		float perimeter = GetPerimeter();
		while (true)
		{
			Vector2 point1 = GetPointOnPerimeter(Random.Range(0, perimeter));
			Vector2 point2 = GetPointOnPerimeter(Random.Range(0, perimeter));
			Vector2 output = (point1 + point2) / 2;
			if (!checkIfContained || Contains_Polygon(output, containsEdges, checkDistance))
				return output;
		}
	}

	public Vector2 GetClosestPoint (Vector2 point, float checkDistance = 99999)
	{
		(Vector2 point, float distanceSqr) closestPointAndDistanceSqr = GetClosestPointAndDistanceSqr(point, checkDistance);
		return closestPointAndDistanceSqr.point;
	}

	public float GetDistanceSqr (Vector2 point, float checkDistance = 99999)
	{
		(Vector2 point, float distanceSqr) closestPointAndDistanceSqr = GetClosestPointAndDistanceSqr(point, checkDistance);
		return closestPointAndDistanceSqr.distanceSqr;
	}

	public (Vector2, float) GetClosestPointAndDistanceSqr (Vector2 point, float checkDistance = 99999)
	{
		if (Contains_Polygon(point, checkDistance: checkDistance))
			return (point, 0);
		else
		{
			Vector2 closestPoint = new Vector2();
			float closestDistanceSqr = Mathf.Infinity;
			float distanceSqr = 0;
			for (int i = 0; i < edges.Length; i ++)
			{
				LineSegment2D edge = edges[i];
				Vector2 pointOnPerimeter = edge.GetClosestPoint(point);
				distanceSqr = (point - pointOnPerimeter).sqrMagnitude;
				if (distanceSqr < closestDistanceSqr)
				{
					closestDistanceSqr = distanceSqr;
					closestPoint = pointOnPerimeter;
				}
			}
			return (closestPoint, closestDistanceSqr);
		}
	}

	public bool DoIIntersectWithShape (Shape2D shape, bool equalPointsIntersect = true)
	{
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			if (shape.DoIIntersectWithLineSegment(edge))
				return true;
		}
		return false;
	}

	public Vector2[] GetIntersectionsWithShape (Shape2D shape)
	{
		List<Vector2> output = new List<Vector2>();
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			for (int i2 = 0; i2 < shape.edges.Length; i2 ++)
			{
				LineSegment2D edge2 = shape.edges[i2];
				Vector2 intersection;
				if (edge.GetIntersectionWithLineSegment(edge2, out intersection))
					output.Add(intersection);
			}
		}
		return output.ToArray();
	}

	public Shape2D Move (Vector2 move)
	{
		for (int i = 0; i < corners.Length; i ++)
			corners[i] = corners[i] + move;
		return new Shape2D(corners);
	}

	public Shape2D Subdivide ()
	{
		List<LineSegment2D> output = new List<LineSegment2D>();
		for (int i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			output.Add(new LineSegment2D(edge.start, edge.GetMidpoint()));
			output.Add(new LineSegment2D(edge.GetMidpoint(), edge.end));
		}
		return new Shape2D(output.ToArray());
	}

	public Shape2D Combine (Shape2D shape)
	{
		throw new NotImplementedException();
	}

	public Shape2D Intersection_Polygon (Shape2D shape)
	{
		throw new NotImplementedException();
	}

	public Shape2D Boolean_Polygon (Shape2D ouptutCanOnlyBeInsideMe)
	{
		throw new NotImplementedException();
	}

	public Shape2D Trim_ConvexPolygon (LineSegment2D lineSegment, bool trimClockwiseSideOfLineSegmentStart)
	{
		List<Vector2> outputCorners = new List<Vector2>(corners);
		List<Vector2> intersections = new List<Vector2>();
		LineSegment2D perpendicularLineSegment = lineSegment.GetPerpendicular(trimClockwiseSideOfLineSegmentStart);
		for (uint i = 0; i < edges.Length; i ++)
		{
			LineSegment2D edge = edges[i];
			Vector2 intersection;
			if (edge.GetIntersectionWithLineSegment(lineSegment, out intersection))
			{
				uint previousCornerIndex = i;
				uint nextCornerIndex = i + 1;
				if (i == edges.Length - 1)
					nextCornerIndex = 0;
				if (perpendicularLineSegment.GetDirectedDistanceAlongParallel(corners[nextCornerIndex]) > lineSegment.GetLength() / 2)
					outputCorners.Insert((int) nextCornerIndex + intersections.Count, intersection);
				else
					outputCorners.Insert((int) previousCornerIndex + intersections.Count, intersection);
				intersections.Add(intersection);
			}
		}
		if (intersections.Count > 0)
		{
			for (int i = 0; i < outputCorners.Count; i ++)
			{
				Vector2 outputCorner = outputCorners[i];
				if (!intersections.Contains(outputCorner) && perpendicularLineSegment.GetDirectedDistanceAlongParallel(outputCorner) > lineSegment.GetLength() / 2)
				{
					outputCorners.RemoveAt(i);
					i --;
				}
			}
		}
		return new Shape2D(outputCorners.ToArray());
	}
}