using System;

namespace Extensions
{
	public static class BoolExtensions
	{
		public static int PositiveOrNegative (this bool b)
		{
			return (int) (((float) b.GetHashCode() - 0.5f) * 2);
		}
	}
}