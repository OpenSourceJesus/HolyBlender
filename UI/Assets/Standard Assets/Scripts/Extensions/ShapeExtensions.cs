using UnityEngine;

namespace Extensions
{
	public static class ShapeExtensions
	{
		public static Shape2D GetShape (this Rigidbody2D rigid)
		{
			Shape2D output = new Shape2D();
			return output;
		}
	}
}