using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class BoundsExtensions
	{
		public static Bounds INFINITE = new Bounds(VectorExtensions.INFINITE3, VectorExtensions.INFINITE3);

		public static bool IsEncapsulating (this Bounds b1, Bounds b2, bool equalBoundsRetunsTrue)
		{
			if (equalBoundsRetunsTrue)
			{
				bool minIsOk = b1.min.x <= b2.min.x && b1.min.y <= b2.min.y && b1.min.z <= b2.min.z;
				bool maxIsOk = b1.min.x >= b2.min.x && b1.min.y >= b2.min.y && b1.min.z >= b2.min.z;
				return minIsOk && maxIsOk;
			}
			else
			{
				bool minIsOk = b1.min.x < b2.min.x && b1.min.y < b2.min.y && b1.min.z < b2.min.z;
				bool maxIsOk = b1.max.x > b2.max.x && b1.max.y > b2.max.y && b1.max.z > b2.max.z;
				return minIsOk && maxIsOk;
			}
		}
		
		public static Bounds Combine (this Bounds[] boundsArray)
		{
			Bounds output = boundsArray[0];
			for (int i = 1; i < boundsArray.Length; i ++)
			{
				Bounds bounds = boundsArray[i];
				output.min = Vector3.Min(bounds.min, output.min);
				output.max = Vector3.Max(bounds.max, output.max);
			}
			return output;
		}
		
		public static BoundsInt Combine (this BoundsInt[] boundsArray)
		{
			BoundsInt output = boundsArray[0];
			for (int i = 1; i < boundsArray.Length; i ++)
			{
				BoundsInt bounds = boundsArray[i];
				output.min = Vector3Int.Min(bounds.min, output.min);
				output.max = Vector3Int.Max(bounds.max, output.max);
			}
			return output;
		}
		
		public static bool Intersects (Bounds b1, Bounds b2, Vector3 expandB1 = new Vector3(), Vector3 expandB2 = new Vector3())
		{
			b1.Expand(expandB1);
			b2.Expand(expandB2);
			return b1.Intersects(b2);
		}
		
		public static float GetVolume (this Bounds b)
		{
			return b.size.x * b.size.y * b.size.z;
		}
		
		public static int GetVolume (this BoundsInt b)
		{
			return b.size.x * b.size.y * b.size.z;
		}
		
		public static Vector3 FromNormalizedPoint (this Bounds b, Vector3 normalizedPoint)
		{
			return b.min + b.size.Multiply(normalizedPoint);
		}
		
		public static Vector3 ToNormalizedPoint (this Bounds b, Vector3 point)
		{
			return point.Divide(b.size) - b.min;
		}
		
		public static Vector3 FlipPoint (this Bounds b, Vector3 point)
		{
			return b.FromNormalizedPoint(Vector3.one - b.ToNormalizedPoint(point));
		}
		
		public static BoundsInt ToBoundsInt (this Bounds b, MathfExtensions.RoundingMethod minRoundingMethod = MathfExtensions.RoundingMethod.HalfOrLessRoundsUp, MathfExtensions.RoundingMethod maxRoundingMethod = MathfExtensions.RoundingMethod.HalfOrMoreRoundsDown)
		{
			BoundsInt output = new BoundsInt();
			output.SetMinMax(b.min.ToVec3Int(minRoundingMethod), b.max.ToVec3Int(maxRoundingMethod));
			return output;
		}
		
		public static Vector3[] GetCorners (this Bounds b)
		{
			Vector3[] corners = new Vector3[8];
			corners[0] = b.min;
			corners[1] = new Vector3(b.max.x, b.min.y, b.min.z);
			corners[2] = new Vector3(b.max.x, b.max.y, b.min.z);
			corners[3] = b.max;
			corners[4] = new Vector3(b.min.x, b.max.y, b.min.z);
			corners[5] = new Vector3(b.min.x, b.max.y, b.max.z);
			corners[6] = new Vector3(b.min.x, b.min.y, b.max.z);
			corners[7] = new Vector3(b.max.x, b.min.y, b.max.z);
			return corners;
		}
		
		public static LineSegment3D[] GetSides (this Bounds b)
		{
			LineSegment3D[] sides = new LineSegment3D[12];
			Vector3[] corners = b.GetCorners();
			Vector3 corner0 = corners[0];
			Vector3 corner1 = corners[1];
			Vector3 corner2 = corners[2];
			Vector3 corner3 = corners[3];
			Vector3 corner4 = corners[4];
			Vector3 corner5 = corners[5];
			Vector3 corner6 = corners[6];
			Vector3 corner7 = corners[7];
			sides[0] = new LineSegment3D(corner0, corner1);
			sides[1] = new LineSegment3D(corner2, corner3);
			sides[2] = new LineSegment3D(corner0, corner6);
			sides[3] = new LineSegment3D(corner6, corner7);
			sides[4] = new LineSegment3D(corner5, corner6);
			sides[5] = new LineSegment3D(corner3, corner5);
			sides[6] = new LineSegment3D(corner3, corner7);
			sides[7] = new LineSegment3D(corner0, corner4);
			sides[8] = new LineSegment3D(corner4, corner5);
			sides[9] = new LineSegment3D(corner2, corner4);
			sides[10] = new LineSegment3D(corner1, corner7);
			sides[11] = new LineSegment3D(corner1, corner2);
			return sides;
		}

		public static Plane[] GetOutsideFacePlanes (this Bounds b)
		{
			Plane[] facePlanes = new Plane[6];
			Vector3[] corners = b.GetCorners();
			Vector3 corner0 = corners[0];
			Vector3 corner1 = corners[1];
			Vector3 corner2 = corners[2];
			Vector3 corner3 = corners[3];
			Vector3 corner4 = corners[4];
			Vector3 corner5 = corners[5];
			Vector3 corner6 = corners[6];
			Vector3 corner7 = corners[7];
			facePlanes[0] = new Plane(corner0, corner5, corner4); // -x
			facePlanes[1] = new Plane(corner1, corner2, corner3); // +x
			facePlanes[2] = new Plane(corner0, corner1, corner6); // -y
			facePlanes[3] = new Plane(corner2, corner4, corner3); // +y
			facePlanes[4] = new Plane(corner0, corner2, corner1); // -z
			facePlanes[5] = new Plane(corner3, corner5, corner6); // +z
			return facePlanes;
		}
		
		public static Vector3[] GetPointsInside (this Bounds b, Vector3 checkInterval)
		{
			List<Vector3> output = new List<Vector3>();
			for (float x = b.min.x; x <= b.max.x; x += checkInterval.x)
			{
				for (float y = b.min.y; y <= b.max.y; y += checkInterval.y)
				{
					for (float z = b.min.z; z <= b.max.z; z += checkInterval.z)
						output.Add(new Vector3(x, y, z));
				}
			}
			return output.ToArray();
		}
		
		public static Vector3[] GetPointsInside (this Bounds b, Vector3 checkInterval, BoundsOffset boundsOffset)
		{
			List<Vector3> output = new List<Vector3>();
			for (float x = b.min.x + boundsOffset.offsetMin.x; x <= b.max.x + boundsOffset.offsetMax.x; x += checkInterval.x)
			{
				for (float y = b.min.y + boundsOffset.offsetMin.y; y <= b.max.y + boundsOffset.offsetMax.y; y += checkInterval.y)
				{
					for (float z = b.min.z + boundsOffset.offsetMin.z; z <= b.max.z + boundsOffset.offsetMax.z; z += checkInterval.z)
						output.Add(new Vector3(x, y, z));
				}
			}
			return output.ToArray();
		}
		
		public static Bounds GetBoundsFromNormalizedMinMax (this Bounds b, Vector3 normalizedStart, Vector3 normalizedEnd)
		{
			Bounds output = new Bounds();
			output.SetMinMax(b.FromNormalizedPoint(normalizedStart), b.FromNormalizedPoint(normalizedEnd));
			return output;
		}
		
		public static Bounds ToBounds (this BoundsInt b)
		{
			return new Bounds(b.min, b.size);
		}
		
		public static Bounds MakePositiveSize (this Bounds b)
		{
			return new Bounds(b.min, b.size.MakePositive());
		}
		
		public static bool Raycast (this Bounds b, Ray ray, out Vector3 hit)
		{
			hit = VectorExtensions.INFINITE3;
			Plane[] facePlanes = b.GetOutsideFacePlanes();
			Plane facePlane0 = facePlanes[0];
			Plane facePlane1 = facePlanes[1];
			Plane facePlane2 = facePlanes[2];
			Plane facePlane3 = facePlanes[3];
			Plane facePlane4 = facePlanes[4];
			Plane facePlane5 = facePlanes[5];
			float distance0 = 0;
			float distance1 = 0;
			float distance2 = 0;
			float distance3 = 0;
			float distance4 = 0;
			float distance5 = 0;
			Vector3 hit0 = new Vector3();
			Vector3 hit1 = new Vector3();
			Vector3 hit2 = new Vector3();
			Vector3 hit3 = new Vector3();
			Vector3 hit4 = new Vector3();
			Vector3 hit5 = new Vector3();
			if (facePlane0.Raycast(ray, out distance0))
			{
				hit0 = ray.GetPoint(distance0);
				if (hit0.y < b.min.y || hit0.y > b.max.y || hit0.z < b.min.z || hit0.z > b.max.z)
					distance0 = Mathf.Infinity;
			}
			else
				distance0 = Mathf.Infinity;
			if (facePlane1.Raycast(ray, out distance1))
			{
				hit1 = ray.GetPoint(distance1);
				if (hit1.y < b.min.y || hit1.y > b.max.y || hit1.z < b.min.z || hit1.z > b.max.z)
					distance1 = Mathf.Infinity;
			}
			else
				distance1 = Mathf.Infinity;
			if (facePlane2.Raycast(ray, out distance2))
			{
				hit2 = ray.GetPoint(distance2);
				if (hit2.x < b.min.x || hit2.x > b.max.x || hit2.z < b.min.z || hit2.z > b.max.z)
					distance2 = Mathf.Infinity;
			}
			else
				distance2 = Mathf.Infinity;
			if (facePlane3.Raycast(ray, out distance3))
			{
				hit3 = ray.GetPoint(distance3);
				if (hit3.x < b.min.x || hit3.x > b.max.x || hit3.z < b.min.z || hit3.z > b.max.z)
					distance3 = Mathf.Infinity;
			}
			else
				distance3 = Mathf.Infinity;
			if (facePlane4.Raycast(ray, out distance4))
			{
				hit4 = ray.GetPoint(distance4);
				if (hit4.x < b.min.x || hit4.x > b.max.x || hit4.y < b.min.y || hit4.y > b.max.y)
					distance4 = Mathf.Infinity;
			}
			else
				distance4 = Mathf.Infinity;
			if (facePlane5.Raycast(ray, out distance5))
			{
				hit5 = ray.GetPoint(distance5);
				if (hit5.x < b.min.x || hit5.x > b.max.x || hit5.y < b.min.y || hit5.y > b.max.y)
					distance5 = Mathf.Infinity;
			}
			else
				distance5 = Mathf.Infinity;
			float distance = Mathf.Min(distance0, distance1, distance2, distance3, distance4, distance5);
			if (distance == Mathf.Infinity)
				return false;
			else if (distance == distance0)
				hit = hit0;
			else if (distance == distance1)
				hit = hit1;
			else if (distance == distance2)
				hit = hit2;
			else if (distance == distance3)
				hit = hit3;
			else if (distance == distance4)
				hit = hit4;
			else
				hit = hit5;
			return true;
		}
		
		public static Vector3 RandomPoint (this Bounds b)
		{
			return new Vector3(Random.Range(b.min.x, b.max.x), Random.Range(b.min.y, b.max.y), Random.Range(b.min.z, b.max.z));
		}
		
		public static BoundsInt Move (this BoundsInt b, Vector3Int move)
		{
			b.position += move;
			return b;
		}
		
		public static Rect ToRect (this Bounds bounds)
		{
			return Rect.MinMaxRect(bounds.min.x, bounds.min.y, bounds.max.x, bounds.max.y);
		}
		
		public static RectInt ToRectInt (this BoundsInt b)
		{
			RectInt output = new RectInt();
			output.SetMinMax((Vector2Int) b.min, (Vector2Int) b.max);
			return output;
		}
		
		public static Bounds Shrink (this Bounds b, Vector3 shrinkBy)
		{
			Bounds output = b;
			output.Expand(-shrinkBy);
			return output;
		}
		
		public static Bounds Shrink (this Bounds b, Bounds shrinkBy)
		{
			Bounds output = b;
			output.Expand(-shrinkBy.size);
			return output;
		}
	}
}