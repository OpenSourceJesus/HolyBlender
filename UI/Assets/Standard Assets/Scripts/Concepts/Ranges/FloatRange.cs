/*
	This file defines a Range of floats
*/

using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[Serializable]
public class FloatRange : Range<float>
{
	public FloatRange ()
	{
	}

	public FloatRange (float min, float max) : base (min, max)
	{
	}

	public bool DoesIntersect (FloatRange floatRange, bool equalFloatsIntersect = true)
	{
		if (equalFloatsIntersect)
			return (min >= floatRange.min && min <= floatRange.max) || (floatRange.min >= min && floatRange.min <= max) || (max <= floatRange.max && max >= floatRange.min) || (floatRange.max <= max && floatRange.max >= min);
		else
			return (min > floatRange.min && min < floatRange.max) || (floatRange.min > min && floatRange.min < max) || (max < floatRange.max && max > floatRange.min) || (floatRange.max < max && floatRange.max > min);
	}

	public bool GetIntersectionRange (FloatRange floatRange, out FloatRange? intersectionRange, bool equalFloatsIntersect = true)
	{
		intersectionRange = null;
		if (DoesIntersect(floatRange, equalFloatsIntersect))
			intersectionRange = new FloatRange(Mathf.Max(min, floatRange.min), Mathf.Min(max, floatRange.max));
		return intersectionRange != null;
	}

	public override float Get (float normalizedValue)
	{
		return (max - min) * normalizedValue + min;
	}

	public override float InverseGet (float value)
	{
		return (value - min) / (max - min);
	}

	public override bool Contains (float value, bool includeMinAndMax = true)
	{
		if (includeMinAndMax)
			return value >= min && value <= max;
		else
			return value > min && value < max;
	}

	public float Clamp (float value)
	{
		return Mathf.Clamp(value, min, max);
	}
}