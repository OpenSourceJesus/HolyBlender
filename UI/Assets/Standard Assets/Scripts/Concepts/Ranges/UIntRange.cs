/*
	This file defines a Range of uints
*/

using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[Serializable]
public class UIntRange : Range<uint>
{
	public UIntRange ()
	{
	}

	public UIntRange (uint min, uint max) : base (min, max)
	{
	}

	public bool DoesIntersect (UIntRange uintRange, bool equalIntsIntersect = true)
	{
		if (equalIntsIntersect)
			return (min >= uintRange.min && min <= uintRange.max) || (uintRange.min >= min && uintRange.min <= max) || (max <= uintRange.max && max >= uintRange.min) || (uintRange.max <= max && uintRange.max >= min);
		else
			return (min > uintRange.min && min < uintRange.max) || (uintRange.min > min && uintRange.min < max) || (max < uintRange.max && max > uintRange.min) || (uintRange.max < max && uintRange.max > min);
	}

	public bool GetIntersectionRange (UIntRange uintRange, out UIntRange? intersectionRange, bool equalIntsIntersect = true)
	{
		intersectionRange = null;
		if (DoesIntersect(uintRange, equalIntsIntersect))
			intersectionRange = new UIntRange((uint) Mathf.Max(min, uintRange.min), (uint) Mathf.Min(max, uintRange.max));
		return intersectionRange != null;
	}

	public override uint Get (float normalizedValue)
	{
		return (uint) Mathf.RoundToInt((max - min) * normalizedValue + min);
	}

	public override bool Contains (uint value, bool includeMinAndMax = true)
	{
		if (includeMinAndMax)
			return value >= min && value <= max;
		else
			return value > min && value < max;
	}
}