using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class PhysicsExtensions
	{
		public static RaycastHit2D LinecastWithWidth (Vector2 start, Vector2 end, float width, int layerMask)
		{
			return Physics2D.BoxCast((start + end) / 2, new Vector2(Vector2.Distance(start, end), width), (end - start).GetFacingAngle(), end - start, Vector2.Distance(start, end), layerMask);
		}

		public static RaycastHit2D[] LinecastAllWithWidth (Vector2 start, Vector2 end, float width, int layerMask)
		{
			return Physics2D.BoxCastAll((start + end) / 2, new Vector2(Vector2.Distance(start, end), width), (end - start).GetFacingAngle(), end - start, Vector2.Distance(start, end), layerMask);
		}
		
		public static int LinecastWithWidth (Vector2 start, Vector2 end, float width, ContactFilter2D contactFilter, RaycastHit2D[] results)
		{
			return Physics2D.BoxCast((start + end) / 2, new Vector2(Vector2.Distance(start, end), width), (end - start).GetFacingAngle(), end - start, contactFilter, results, Vector2.Distance(start, end));
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

		public static bool LayersCollideWithSameLayers (this int layer1, int layer2)
		{
			bool output = false;
			LayerMask collisionMask1 = (LayerMask) Physics2D.GetLayerCollisionMask(layer1);
			LayerMask collisionMask2 = (LayerMask) Physics2D.GetLayerCollisionMask(layer2);
			string[] collisionMask1LayerNames = collisionMask1.ToLayerNames();
			string[] collisionMask2LayerNames = collisionMask2.ToLayerNames();
			output = collisionMask1 == collisionMask2 || (collisionMask1.Contains(layer1) == collisionMask2.Contains(layer1) && collisionMask1.Contains(layer2) == collisionMask2.Contains(layer2) && collisionMask1LayerNames.Remove(LayerMask.LayerToName(layer1)).Remove(LayerMask.LayerToName(layer2)) == collisionMask2LayerNames.Remove(LayerMask.LayerToName(layer1)).Remove(LayerMask.LayerToName(layer2)));
			return output;
		}
	}
}