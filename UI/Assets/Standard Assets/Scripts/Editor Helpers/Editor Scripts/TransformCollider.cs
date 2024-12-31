#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;

namespace HolyBlender
{
	public class TransformCollider : EditorScript
	{
		public Collider2D collider;
		public Transform trs;

		public override void Do ()
		{
			if (collider == null)
				collider = GetComponent<Collider2D>();
			Transform oldTrs = collider.transform;
			PolygonCollider2D polygonCollider = collider as PolygonCollider2D;
			if (polygonCollider != null)
			{
				Vector2[] points = polygonCollider.points;
				for (int i = 0; i < points.Length; i ++)
				{
					Vector2 point = points[i];
					point = oldTrs.InverseTransformPoint(point);
					point = trs.TransformPoint(point);
					points[i] = point;
				}
				polygonCollider.points = points;
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class TransformCollider : EditorScript
	{
	}
}
#endif