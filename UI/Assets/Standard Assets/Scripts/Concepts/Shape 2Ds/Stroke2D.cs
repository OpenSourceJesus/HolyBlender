using System;
using Extensions;
using UnityEngine;
using System.Collections.Generic;

[Serializable]
public class Stroke2D : Shape2D
{
	public Vector2 startPoint;
	public Vector2 startDirection;
	public ControlPoint[] controlPoints = new ControlPoint[0];
	public AnimationCurve turnRateCurve;
	public AnimationCurve widthCurve;
	public float length;
	public float[] sampleIntervals = new float[0];

	public Stroke2D ()
	{
	}

	public Stroke2D (Vector2 startPoint, Vector2 startDirection, ControlPoint[] controlPoints, AnimationCurve turnRateCurve, AnimationCurve widthCurve, float length, float[] sampleIntervals)
	{
		this.startPoint = startPoint;
		this.startDirection = startDirection;
		this.controlPoints = controlPoints;
		this.turnRateCurve = turnRateCurve;
		this.widthCurve = widthCurve;
		this.length = length;
		this.sampleIntervals = sampleIntervals;
		SetCorners ();
		SetEdges_Polygon ();
	}

	public Stroke2D (Vector2 startPoint, Vector2 startDirection, ControlPoint[] controlPoints, AnimationCurve turnRateCurve, AnimationCurve widthCurve, float length, float sampleInterval) : this (startPoint, startDirection, controlPoints, turnRateCurve, widthCurve, length, new float[1] { sampleInterval })
	{
	}

	void SetCorners ()
	{
		float lengthTraveled = 0;
		float normalizedLengthTraveled = lengthTraveled / length;
		List<Vector2> firstCorners = new List<Vector2>();
		List<Vector2> secondCorners = new List<Vector2>();
		Vector2 forward = startDirection.normalized;
		Vector2 position = startPoint;
		int controlPointIndex = 0;
		ControlPoint controlPoint = controlPoints[0];
		ControlPoint nextControlPoint = null;
		if (controlPoints.Length > 1)
			nextControlPoint = controlPoints[1];
		int positionIndex = 0;
		while (true)
		{
			float radius = widthCurve.Evaluate(normalizedLengthTraveled) / 2;
			float turnRate = turnRateCurve.Evaluate(normalizedLengthTraveled);
			Vector2 tangent = forward.Rotate90();
			firstCorners.Add(position - tangent * radius);
			secondCorners.Insert(0, position + tangent * radius);
			float sampleInterval = sampleIntervals[positionIndex];
			forward = forward.RotateTo(controlPoint.point - position, turnRate * sampleInterval);
			lengthTraveled += sampleInterval;
			normalizedLengthTraveled = lengthTraveled / length;
			if (nextControlPoint != null && lengthTraveled >= nextControlPoint.startUsingAtLength)
			{
				controlPoint = nextControlPoint;
				controlPointIndex ++;
				if (controlPoints.Length > controlPointIndex)
					nextControlPoint = controlPoints[controlPointIndex];
			}
			if (lengthTraveled >= length)
				break;
			position += forward * sampleInterval;
			if (positionIndex < sampleIntervals.Length - 1)
				positionIndex ++;
		}
		firstCorners.AddRange(secondCorners);
		corners = firstCorners.ToArray();
	}

	public Stroke2D Move (Vector2 movement)
	{
		Stroke2D output = new Stroke2D();
		output.corners = new Vector2[corners.Length];
		for (int i = 0; i < corners.Length; i ++)
			output.corners[i] = corners[i] + movement;
		output.SetEdges_Polygon ();
		output.startPoint += movement;
		output.widthCurve = widthCurve;
		output.turnRateCurve = turnRateCurve;
		output.length = length;
		output.sampleIntervals = sampleIntervals;
		output.controlPoints = new ControlPoint[controlPoints.Length];
		for (int i = 0; i < controlPoints.Length; i ++)
		{
			ControlPoint controlPoint = controlPoints[i];
			controlPoint.point += movement;
			output.controlPoints[i] = controlPoint;
		}
		return output;
	}

	public Stroke2D Rotate (Vector2 pivotPoint, float degrees)
	{
		Stroke2D output = new Stroke2D();
		output.corners = new Vector2[corners.Length];
		for (int i = 0; i < corners.Length; i ++)
			output.corners[i] = corners[i].Rotate(pivotPoint, degrees);
		output.SetEdges_Polygon ();
		output.startPoint = startPoint.Rotate(pivotPoint, degrees);
		output.startDirection = startDirection.Rotate(degrees);
		output.widthCurve = widthCurve;
		output.turnRateCurve = turnRateCurve;
		output.length = length;
		output.sampleIntervals = sampleIntervals;
		output.controlPoints = new ControlPoint[controlPoints.Length];
		for (int i = 0; i < controlPoints.Length; i ++)
		{
			ControlPoint controlPoint = controlPoints[i];
			controlPoint.point = controlPoint.point.Rotate(pivotPoint, degrees);
			output.controlPoints[i] = controlPoint;
		}
		return output;
	}

	public Stroke2D Rotate (float degrees)
	{
		Stroke2D output = new Stroke2D();
		output.corners = new Vector2[corners.Length];
		for (int i = 0; i < corners.Length; i ++)
			output.corners[i] = corners[i].Rotate(degrees);
		output.SetEdges_Polygon ();
		output.startPoint = startPoint.Rotate(degrees);
		output.startDirection = startDirection.Rotate(degrees);
		output.widthCurve = widthCurve;
		output.turnRateCurve = turnRateCurve;
		output.length = length;
		output.sampleIntervals = sampleIntervals;
		output.controlPoints = new ControlPoint[controlPoints.Length];
		for (int i = 0; i < controlPoints.Length; i ++)
		{
			ControlPoint controlPoint = controlPoints[i];
			controlPoint.point = controlPoint.point.Rotate(degrees);
			output.controlPoints[i] = controlPoint;
		}
		return output;
	}

	public static Stroke2D Straight (Vector2 startPoint, Vector2 endPoint, float width)
	{
		AnimationCurve widthCurve = new AnimationCurve(new Keyframe(0, width));
		Vector2 toEndPoint = endPoint - startPoint;
		float length = toEndPoint.magnitude;
		return new Stroke2D(startPoint, toEndPoint, new ControlPoint[1] { new ControlPoint() }, new AnimationCurve(), widthCurve, length, new float[1] { length });
	}

	public static Stroke2D FromPoints (AnimationCurve widthCurve, params Vector2[] points)
	{
		float[] sampleIntervals = new float[points.Length - 1];
		ControlPoint[] controlPoints = new ControlPoint[points.Length - 1];
		float length = 0;
		AnimationCurve turnRateCurve = new AnimationCurve(new Keyframe(0, 99999));
		Vector2 startPoint = points[0];
		// controlPoints[0] = new ControlPoint(startPoint, 0);
		Vector2 previousPoint = startPoint;
		for (int i = 1; i < points.Length; i ++)
		{
			Vector2 point = points[i];
			Vector2 toPoint = point - previousPoint;
			sampleIntervals[i - 1] = toPoint.magnitude;
			controlPoints[i - 1] = new ControlPoint(point, length);
			length += toPoint.magnitude;
			previousPoint = point;
		}
		return new Stroke2D(startPoint, points[1] - startPoint, controlPoints, turnRateCurve, widthCurve, length, sampleIntervals);
	}

	public static Stroke2D FromPoints (AnimationCurve widthCurve, float sampleInterval, params Vector2[] points)
	{
		ControlPoint[] controlPoints = new ControlPoint[points.Length - 1];
		float length = 0;
		AnimationCurve turnRateCurve = new AnimationCurve(new Keyframe(0, 99999));
		Vector2 startPoint = points[0];
		// controlPoints[0] = new ControlPoint(startPoint, 0);
		Vector2 previousPoint = startPoint;
		for (int i = 1; i < points.Length; i ++)
		{
			Vector2 point = points[i];
			Vector2 toPoint = point - previousPoint;
			controlPoints[i - 1] = new ControlPoint(point, length);
			length += toPoint.magnitude;
			previousPoint = point;
		}
		return new Stroke2D(startPoint, points[1] - startPoint, controlPoints, turnRateCurve, widthCurve, length, sampleInterval);
	}

	[Serializable]
	public class ControlPoint
	{
		public Vector2 point;
		public float startUsingAtLength;

		public ControlPoint ()
		{
		}

		public ControlPoint (Vector2 point, float startUsingAtLength)
		{
			this.point = point;
			this.startUsingAtLength = startUsingAtLength;
		}
	}
}