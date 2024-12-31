using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class ColorExtensions
	{
		public static Color SetAlpha (this Color c, float a)
		{
			return new Color(c.r, c.g, c.b, a);
		}
		
		public static Color AddAlpha (this Color c, float a)
		{
			return c.SetAlpha(c.a + a);
		}
		
		public static Color MultiplyAlpha (this Color c, float a)
		{
			return c.SetAlpha(c.a * a);
		}
		
		public static Color DivideAlpha (this Color c, float a)
		{
			return c.SetAlpha(c.a / a);
		}
		
		public static Color Add (this Color c, float f)
		{
			c.r += f;
			c.g += f;
			c.b += f;
			return c;
		}
		
		public static Color Multiply (this Color c, float f)
		{
			c.r *= f;
			c.g *= f;
			c.b *= f;
			return c;
		}
		
		public static Color Divide (this Color c, float f)
		{
			c.r /= f;
			c.g /= f;
			c.b /= f;
			return c;
		}

		public static Color RandomColor ()
		{
			return new Color(Random.value, Random.value, Random.value);
		}

		public static float InverseLerp (Color from, Color to, Color value)
		{
			return VectorExtensions.InverseLerp(from, to, value);
		}

		public static float GetDifference (this Color color, Color color2)
		{
			float dR = Mathf.Abs(color.r - color2.r);
			float dG = Mathf.Abs(color.g - color2.g);
			float dB = Mathf.Abs(color.b - color2.b);
			return (dR + dG + dB) / 3;
		}
	}
}