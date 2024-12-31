using System;
using UnityEngine;

[Serializable]
public struct ColorOffset
{
	public ComponentOffset redOffset;
	public ComponentOffset greenOffset;
	public ComponentOffset blueOffset;
	public ComponentOffset alphaOffset;

	public Color Apply (Color color)
	{
		return new Color(redOffset.Apply(color.r), greenOffset.Apply(color.g), blueOffset.Apply(color.b));
	}

	public Color ApplyWithTransparency (Color color)
	{
		Color output = Apply(color);
		output.a = alphaOffset.Apply(color.a);
		return output;
	}

	public Color ApplyInverse (Color color)
	{
		return new Color(redOffset.ApplyInverse(color.r), greenOffset.ApplyInverse(color.g), blueOffset.ApplyInverse(color.b));
	}

	public Color ApplyInverseWithTransparency (Color color)
	{
		Color output = ApplyInverse(color);
		output.a = alphaOffset.ApplyInverse(color.a);
		return output;
	}

	[Serializable]
	public struct ComponentOffset
	{
		public Operation operation;
		public float value;

		public float Apply (float component)
		{
			if (operation == Operation.Add)
				return component + value;
			else if (operation == Operation.Subtract)
				return component - value;
			else if (operation == Operation.Multiply)
				return component * value;
			else// if (operation == Operation.Divide)
				return component / value;
		}

		public float ApplyInverse (float component)
		{
			if (operation == Operation.Add)
				return component - value;
			else if (operation == Operation.Subtract)
				return component + value;
			else if (operation == Operation.Multiply)
				return component / value;
			else// if (operation == Operation.Divide)
				return component * value;
		}
	}

	public enum Operation
	{
		Add,
		Subtract,
		Multiply,
		Divide
	}
}
