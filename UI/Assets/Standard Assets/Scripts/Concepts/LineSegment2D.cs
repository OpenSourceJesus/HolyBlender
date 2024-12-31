using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[Serializable]
public class LineSegment2D
{
	public Vector2 start;
	public Vector2 end;

	public LineSegment2D ()
	{
	}

	public LineSegment2D (Vector2 start, Vector2 end)
	{
		this.start = start;
		this.end = end;
	}

	public override string ToString ()
	{
		return "[" + start + "], [" + end + "]";
	}

#if UNITY_EDITOR
	public virtual void DrawGizmos (Color color)
	{
		GizmosManager.GizmosEntry gizmosEntry = new GizmosManager.GizmosEntry();
		gizmosEntry.setColor = true;
		gizmosEntry.color = color;
		gizmosEntry.onDrawGizmos += DrawGizmos;
		GizmosManager.gizmosEntries.Add(gizmosEntry);
	}

	public virtual void DrawGizmos (object arg)
	{
		Gizmos.DrawLine(start, end);
	}
#endif
	
	public float GetSlope ()
	{
		return (end.y - start.y) / (end.x - start.x);
	}
	
	public float GetFacingAngle ()
	{
		return (end - start).GetFacingAngle();
	}

	public bool DoIIntersectWithLineSegment (LineSegment2D other, bool equalPointsIntersect)
	{
		bool output = false;
		float denominator = (other.end.y - other.start.y) * (end.x - start.x) - (other.end.x - other.start.x) * (end.y - start.y);
		if (denominator != 0f)
		{
			float u_a = ((other.end.x - other.start.x) * (start.y - other.start.y) - (other.end.y - other.start.y) * (start.x - other.start.x)) / denominator;
			float u_b = ((end.x - start.x) * (start.y - other.start.y) - (end.y - start.y) * (start.x - other.start.x)) / denominator;
			if (equalPointsIntersect)
			{
				if (u_a >= 0f && u_a <= 1f && u_b >= 0f && u_b <= 1f)
					output = true;
			}
			else
			{
				if (u_a > 0f && u_a < 1f && u_b > 0f && u_b < 1f)
					output = true;
			}
		}
		return output;
	}

	public bool DoIIntersectWithCircle (Vector2 center, float radius)
	{
		return Vector2.Distance(GetClosestPoint(center), center) <= radius;
	}

	// public bool DoIIntersectWithCircle (Vector2 center, float radius)
	// {
	// 	return Vector2.Distance(GetPointWithDirectedDistance(GetDirectedDistanceAlongParallel(center)), center) <= radius;
	// }

	// public bool DoIIntersectWithCircle (Vector2 center, float radius)
	// {
	// 	Vector2 lineDirection = GetDirection();
	// 	Vector2 centerToLineStart = start - center;
	// 	float a = Vector2.Dot(lineDirection, lineDirection);
	// 	float b = 2 * Vector2.Dot(centerToLineStart, lineDirection);
	// 	float c = Vector2.Dot(centerToLineStart, centerToLineStart) - radius * radius;
	// 	float discriminant = b * b - 4 * a * c;
	// 	if (discriminant >= 0)
	// 	{
	// 		discriminant = Mathf.Sqrt(discriminant);
	// 		float t1 = (-b - discriminant) / (2 * a);
	// 		float t2 = (-b + discriminant) / (2 * a);
	// 		if (t1 >= 0 && t1 <= 1 || t2 >= 0 && t2 <= 1)
	// 			return true;
	// 	}
	// 	return false;
	// }

	public bool GetIntersectionWithLineSegment (LineSegment2D line, out Vector2 intersection)
	{
		intersection = Vector2.zero;
		float d = (end.x - start.x) * (line.end.y - line.start.y) - (end.y - start.y) * (line.end.x - line.start.x);
		if (d == 0)
			return false;
		float u = ((line.start.x - start.x) * (line.end.y - line.start.y) - (line.start.y - start.y) * (line.end.x - line.start.x)) / d;
		float v = ((line.start.x - start.x) * (end.y - start.y) - (line.start.y - start.y) * (end.x - start.x)) / d;
		if (u < 0 || u > 1 || v < 0 || v > 1)
			return false;
		intersection.x = start.x + u * (end.x - start.x);
		intersection.y = start.y + u * (end.y - start.y);
		return true;
	}
	
	public bool ContainsPoint (Vector2 point)
	{
		return Vector2.Distance(point, start) + Vector2.Distance(point, end) == Vector2.Distance(start, end);
	}
	
	public LineSegment2D Move (Vector2 movement)
	{
		return new LineSegment2D(start + movement, end + movement);
	}
	
	public LineSegment2D Rotate (Vector2 pivotPoint, float degrees)
	{
		Vector2 outputStart = start.Rotate(pivotPoint, degrees);
		Vector2 outputEnd = end.Rotate(pivotPoint, degrees);
		return new LineSegment2D(outputStart, outputEnd);
	}

	public Vector2 GetClosestPoint (Vector2 point)
	{
		Vector2 output;
		float directedDistanceAlongParallel = GetDirectedDistanceAlongParallel(point);
		if (directedDistanceAlongParallel > 0 && directedDistanceAlongParallel < GetLength())
			output = GetPointWithDirectedDistance(directedDistanceAlongParallel);
		else if (directedDistanceAlongParallel >= GetLength())
			output = end;
		else
			output = start;
		return output;
	}

	public LineSegment2D GetPerpendicular (bool rotateClockwise = false)
	{
		if (rotateClockwise)
			return Rotate(GetMidpoint(), -90);
		else
			return Rotate(GetMidpoint(), 90);
	}

	public Vector2 GetMidpoint ()
	{
		return (start + end) / 2;
	}

	public float GetDirectedDistanceAlongParallel (Vector2 point)
	{
		float rotate = -GetFacingAngle();
		LineSegment2D rotatedLine = Rotate(Vector2.zero, rotate);
		point = point.Rotate(rotate);
		return point.x - rotatedLine.start.x;
	}

	public Vector2 GetPointWithDirectedDistance (float directedDistance)
	{
		return start + (GetDirection() * directedDistance);
	}

	public float GetLength ()
	{
		return Vector2.Distance(start, end);
	}

	public Vector2 GetDirection ()
	{
		return (end - start).normalized;
	}
	
	public LineSegment2D Flip ()
	{
		return new LineSegment2D(end, start);
	}
}