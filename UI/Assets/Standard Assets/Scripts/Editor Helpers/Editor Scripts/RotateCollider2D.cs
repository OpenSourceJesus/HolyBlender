#if UNITY_EDITOR
using Extensions;
using UnityEngine;

namespace HolyBlender
{
	public class RotateCollider2D : EditorScript
	{
		public Collider2D collider;
		public float rotation;

		public override void Do ()
		{
			if (collider == null)
				collider = GetComponent<Collider2D>();
			PolygonCollider2D polygonCollider = collider as PolygonCollider2D;
			if (polygonCollider != null)
			{
				Vector2[] points = polygonCollider.points;
				for (int i = 0; i < polygonCollider.points.Length; i ++)
				{
					points[i] = points[i].Rotate(polygonCollider.bounds.center, rotation);
				}
				polygonCollider.points = points;
			}
		}
	}
}
#else
namespace HolyBlender
{
	public class RotateCollider2D : EditorScript
	{
	}
}
#endif