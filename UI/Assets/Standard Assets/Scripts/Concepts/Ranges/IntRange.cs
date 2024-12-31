/*
	This file defines a Range of ints
*/

using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[Serializable]
public class IntRange : Range<int>
{
	public IntRange ()
	{
	}

	public IntRange (int min, int max) : base (min, max)
	{
	}

	public bool DoesIntersect (IntRange intRange, bool equalIntsIntersect = true)
	{
		if (equalIntsIntersect)
			return (min >= intRange.min && min <= intRange.max) || (intRange.min >= min && intRange.min <= max) || (max <= intRange.max && max >= intRange.min) || (intRange.max <= max && intRange.max >= min);
		else
			return (min > intRange.min && min < intRange.max) || (intRange.min > min && intRange.min < max) || (max < intRange.max && max > intRange.min) || (intRange.max < max && intRange.max > min);
	}

	public bool GetIntersectionRange (IntRange intRange, out IntRange? intersectionRange, bool equalIntsIntersect = true)
	{
		intersectionRange = null;
		if (DoesIntersect(intRange, equalIntsIntersect))
			intersectionRange = new IntRange(Mathf.Max(min, intRange.min), Mathf.Min(max, intRange.max));
		return intersectionRange != null;
	}

	public override int Get (float normalizedValue)
	{
		return Mathf.RoundToInt((max - min) * normalizedValue + min);
	}

	public override bool Contains (int value, bool includeMinAndMax = true)
	{
		if (includeMinAndMax)
			return value >= min && value <= max;
		else
			return value > min && value < max;
	}
}