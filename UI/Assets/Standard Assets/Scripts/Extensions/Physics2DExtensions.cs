using System.Collections.Generic;
using UnityEngine;

namespace Extensions
{
	public static class Physics2DExtensions
	{
		public static RaycastHit2D LinecastWithWidth (Vector2 start, Vector2 end, float width, int layerMask)
		{
			float distance = Vector2.Distance(start, end);
			return Physics2D.BoxCast((start + end) / 2, new Vector2(distance, width), (end - start).GetFacingAngle(), end - start, distance, layerMask);
		}

		public static RaycastHit2D[] LinecastAllWithWidth (Vector2 start, Vector2 end, float width, int layerMask)
		{
			float distance = Vector2.Distance(start, end);
			return Physics2D.BoxCastAll((start + end) / 2, new Vector2(distance, width), (end - start).GetFacingAngle(), end - start, distance, layerMask);
		}
		
		public static int LinecastWithWidth (Vector2 start, Vector2 end, float width, ContactFilter2D contactFilter, RaycastHit2D[] results)
		{
			float distance = Vector2.Distance(start, end);
			return Physics2D.BoxCast((start + end) / 2, new Vector2(distance, width), (end - start).GetFacingAngle(), end - start, contactFilter, results, distance);
		}
		
		public static int LinecastWithWidth (Vector2 start, Vector2 end, float width, ContactFilter2D contactFilter, List<RaycastHit2D> results)
		{
			float distance = Vector2.Distance(start, end);
			return Physics2D.BoxCast((start + end) / 2, new Vector2(distance, width), (end - start).GetFacingAngle(), end - start, contactFilter, results, distance);
		}

		public static RaycastHit2D[] LinecastAllWithWidthAndOrder (Vector2 start, Vector2 end, float width, int layerMask)
		{
			LineSegment2D lineSegment = new LineSegment2D(start, end);
			List<RaycastHit2D> hits = new List<RaycastHit2D>();
			RaycastHit2D hit;
			do
			{
				hit = LinecastWithWidth(lineSegment.start, end, width, layerMask);
				if (hit.collider != null)
				{
					lineSegment.start = lineSegment.GetPointWithDirectedDistance(lineSegment.GetDirectedDistanceAlongParallel(hit.point));
					hits.Add(hit);
				}
			} while (hit.collider != null);
			return hits.ToArray();
		}
	}
}