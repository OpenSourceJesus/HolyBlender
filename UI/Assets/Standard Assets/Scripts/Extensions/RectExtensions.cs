using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class RectExtensions
	{
		public static Rect INFINITE = Rect.MinMaxRect(-Mathf.Infinity, -Mathf.Infinity, Mathf.Infinity, Mathf.Infinity);

		public static Rect Move (this Rect rect, Vector2 movement)
		{
			rect.position += movement;
			return rect;
		}
		
		public static RectInt Move (this RectInt rect, Vector2Int movement)
		{
			rect.position += movement;
			return rect;
		}

		public static Rect SwapXAndY (this Rect rect)
		{
			return Rect.MinMaxRect(rect.min.y, rect.min.x, rect.max.y, rect.max.x);
		}
		
		public static bool IsEncapsulating (this Rect r1, Rect r2, bool equalRectsRetunsTrue)
		{
			if (equalRectsRetunsTrue)
			{
				bool minIsOk = r1.min.x <= r2.min.x && r1.min.y <= r2.min.y;
				bool maxIsOk = r1.max.x >= r2.max.x && r1.max.y >= r2.max.y;
				return minIsOk && maxIsOk;
			}
			else
			{
				bool minIsOk = r1.min.x < r2.min.x && r1.min.y < r2.min.y;
				bool maxIsOk = r1.max.x > r2.max.x && r1.max.y > r2.max.y;
				return minIsOk && maxIsOk;
			}
		}
		
		public static bool IsIntersecting (this Rect r1, Rect r2, bool equalRectsRetunsTrue = true)
		{
			if (equalRectsRetunsTrue)
				return r1.xMin <= r2.xMax && r1.xMax >= r2.xMin && r1.yMin <= r2.yMax && r1.yMax >= r2.yMin;
			else
				return r1.xMin < r2.xMax && r1.xMax > r2.xMin && r1.yMin < r2.yMax && r1.yMax > r2.yMin;
		}

		public static Vector2[] GetCorners (this Rect rect)
		{
			Vector2[] output = new Vector2[4];
			output[0] = rect.min;
			output[1] = new Vector2(rect.xMax, rect.yMin);
			output[2] = rect.max;
			output[3] = new Vector2(rect.xMin, rect.yMax);
			return output;
		}
		
		public static LineSegment2D[] GetSides (this Rect rect)
		{
			LineSegment2D[] sides = new LineSegment2D[4];
			Vector2[] corners = rect.GetCorners();
			Vector2 corner0 = corners[0];
			Vector2 corner1 = corners[1];
			Vector2 corner2 = corners[2];
			Vector2 corner3 = corners[3];
			sides[0] = new LineSegment2D(corner0, corner1);
			sides[1] = new LineSegment2D(corner1, corner2);
			sides[2] = new LineSegment2D(corner2, corner3);
			sides[3] = new LineSegment2D(corner3, corner0);
			return sides;
		}
		
		public static bool IsExtendingOutside (this Rect r1, Rect r2, bool equalRectsRetunsTrue)
		{
			if (equalRectsRetunsTrue)
			{
				bool minIsOk = r1.min.x <= r2.min.x || r1.min.y <= r2.min.y;
				bool maxIsOk = r1.max.x >= r2.max.x || r1.max.y >= r2.max.y;
				return minIsOk || maxIsOk;
			}
			else
			{
				bool minIsOk = r1.min.x < r2.min.x || r1.min.y < r2.min.y;
				bool maxIsOk = r1.max.x > r2.max.x || r1.max.y > r2.max.y;
				return minIsOk || maxIsOk;
			}
		}

		public static Rect Combine (this Rect[] rectsArray)
		{
			Rect output = rectsArray[0];
			for (int i = 1; i < rectsArray.Length; i ++)
			{
				Rect rect = rectsArray[i];
				if (rect.min.x < output.min.x)
					output.min = new Vector2(rect.min.x, output.min.y);
				if (rect.min.y < output.min.y)
					output.min = new Vector2(output.min.x, rect.min.y);
				if (rect.max.x > output.max.x)
					output.max = new Vector2(rect.max.x, output.max.y);
				if (rect.max.y > output.max.y)
					output.max = new Vector2(output.max.x, rect.max.y);
			}
			return output;
		}

		public static Rect Expand (this Rect rect, Vector2 amount)
		{
			Vector2 center = rect.center;
			rect.size += amount;
			rect.center = center;
			return rect;
		}
		
		public static Rect Set (this Rect rect, RectInt rectInt)
		{
			rect.center = rectInt.center;
			rect.size = rectInt.size;
			return rect;
		}

		public static Rect ToRect (this RectInt rectInt)
		{
			return Rect.MinMaxRect(rectInt.xMin, rectInt.yMin, rectInt.xMax, rectInt.yMax);
		}

		public static Vector2 ClosestPoint (this Rect rect, Vector2 point)
		{
			return point.ClampComponents(rect.min, rect.max);
		}

		public static Vector2 ToNormalizedPosition (this Rect rect, Vector2 point)
		{
			return Rect.PointToNormalized(rect, point);
			// return Vector2.one.Divide(rect.size) * (point - rect.min);
		}

		public static Vector2 ToNormalizedPosition (this RectInt rect, Vector2Int point)
		{
			return Vector2.one.Divide(rect.size.ToVec2()).Multiply(point.ToVec2() - rect.min.ToVec2());
		}

		public static Rect SetToPositiveSize (this Rect rect)
		{
			Rect output = rect;
			output.size = new Vector2(Mathf.Abs(output.size.x), Mathf.Abs(output.size.y));
			output.center = rect.center;
			return output;
		}

		public static Circle2D GetSmallestCircleAround (this Rect rect)
		{
			return new Circle2D(rect.center, rect.size.magnitude / 2);
		}

		// public static Rect GetExactFitRectForCircle (Circle2D circle)
		// {
		// }

		public static Rect AnchorToPoint (this Rect rect, Vector2 point, Vector2 anchorPoint)
		{
			Rect output = rect;
			output.position = point - (output.size * anchorPoint);
			return output;
		}

		public static LineSegment2D[] GetEdges (this Rect rect)
		{
			return new LineSegment2D[4] { new LineSegment2D(rect.min, new Vector2(rect.xMin, rect.yMax)), new LineSegment2D(rect.min, new Vector2(rect.xMax, rect.yMin)), new LineSegment2D(rect.max, new Vector2(rect.xMin, rect.yMax)), new LineSegment2D(rect.max, new Vector2(rect.xMax, rect.yMin)) };
		}

		public static Bounds ToBounds (this Rect rect)
		{
			return new Bounds(rect.center, rect.size);
		}

		public static Bounds ToBounds (this RectInt rect)
		{
			return new Bounds(rect.center, rect.size.ToVec2());
		}

		public static BoundsInt ToBoundsInt (this RectInt rect, MathfExtensions.RoundingMethod minRoundingMethod = MathfExtensions.RoundingMethod.RoundUpIfNotInteger, MathfExtensions.RoundingMethod maxRoundingMethod = MathfExtensions.RoundingMethod.RoundUpIfNotInteger)
		{
			return rect.ToBounds().ToBoundsInt(minRoundingMethod, maxRoundingMethod);
		}

		public static Rect GrowToPoint (this Rect rect, Vector2 point)
		{
			rect.min = rect.min.SetToMinComponents(point);
			rect.max = rect.max.SetToMaxComponents(point);
			return rect;
		}

		public static float GetPerimeter (this Rect rect)
		{
			return rect.size.x * 2 + rect.size.y * 2;
		}

		public static Vector2 GetPointOnEdges (this Rect rect, float distance)
		{
			if (distance <= rect.size.y)
				return new Vector2(rect.xMin, rect.yMin + distance);
			else if (distance <= rect.size.y + rect.size.x)
				return new Vector2(rect.xMin + distance - rect.size.y, rect.yMax);
			else if (distance <= rect.size.y * 2 + rect.size.x)
				return new Vector2(rect.xMax, rect.yMax - (distance - rect.size.x - rect.size.y));
			else
				return new Vector2(rect.xMax - (distance - rect.size.x - rect.size.y * 2), rect.yMin);
		}
		
		public static Vector2 RandomPoint (this Rect b)
		{
			return new Vector2(Random.Range(b.xMin, b.xMax), Random.Range(b.yMin, b.yMax));
		}

		public static Vector2 ClosestPointOnBoundsOrCenter (this Rect rect, Vector2 point)
		{
			Vector2 closestPoint = rect.ClosestPoint(point);
			Vector2[] corners = rect.GetCorners();
			Vector2 corner0 = corners[0];
			Vector2 corner1 = corners[1];
			Vector2 corner2 = corners[2];
			Vector2 corner3 = corners[3];
			// if (closestPoint.x < )
			return closestPoint;
		}
	}
}