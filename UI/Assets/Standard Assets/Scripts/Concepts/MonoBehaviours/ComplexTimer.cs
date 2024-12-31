using Extensions;
using UnityEngine;
using UnityEngine.UI;
using System.Collections;

namespace HolyBlender
{
	public class ComplexTimer : MonoBehaviour, IUpdatable
	{
		public string title;
		public bool realtime;
		public ClampedFloat value;
		public float changeAmountMultiplier;
		public RepeatType repeatType;
		float timeSinceLastGetValue;
		float previousChangeAmountMultiplier;
		[HideInInspector]
		public float initValue;
		
		public float GetValue ()
		{
			value.SetValue(value.GetValue() + timeSinceLastGetValue * changeAmountMultiplier);
			if ((value.GetValue() == value.valueRange.max && changeAmountMultiplier > 0) || (value.GetValue() == value.valueRange.min && changeAmountMultiplier < 0))
			{
				if (repeatType == RepeatType.Loop)
					JumpToStart ();
				else if (repeatType  == RepeatType.PingPong)
					changeAmountMultiplier *= -1;
			}
			timeSinceLastGetValue = 0;
			return value.GetValue();
		}
		
		public void Awake ()
		{
#if UNITY_EDTIOR
			if (!Application.isPlaying)
				return;
#endif
			if (value == null)
				value = new ClampedFloat();
			initValue = value.GetValue();
			GameManager.updatables = GameManager.updatables.Add(this);
		}
		
		public void DoUpdate ()
		{
			if (realtime)
				UpdateTimer(Time.unscaledDeltaTime);
			else
				UpdateTimer(Time.deltaTime);
		}

		public void OnDestroy ()
		{
#if UNITY_EDTIOR
			if (!Application.isPlaying)
				return;
#endif
			GameManager.updatables = GameManager.updatables.Remove(this);
		}
		
		public void UpdateTimer (float deltaTime)
		{
			timeSinceLastGetValue += deltaTime;
		}
		
		public bool IsAtStart ()
		{
			float timerValue = GetValue();
			return (timerValue == value.valueRange.max && changeAmountMultiplier < 0) || (timerValue == value.valueRange.min && changeAmountMultiplier > 0) || ((timerValue == value.valueRange.min || timerValue == value.valueRange.max) && changeAmountMultiplier == 0);
		}
		
		public bool IsAtEnd ()
		{
			float timerValue = GetValue();
			return (timerValue == value.valueRange.min && changeAmountMultiplier < 0) || (timerValue == value.valueRange.max && changeAmountMultiplier > 0) || ((timerValue == value.valueRange.min || timerValue == value.valueRange.max) && changeAmountMultiplier == 0);
		}
		
		public void Pause ()
		{
			if (changeAmountMultiplier == 0)
				return;
			previousChangeAmountMultiplier = changeAmountMultiplier;
			changeAmountMultiplier = 0;
		}
		
		public void Resume ()
		{
			if (changeAmountMultiplier != 0)
				return;
			changeAmountMultiplier = previousChangeAmountMultiplier;
		}
		
		public void JumpToStart ()
		{
			if (changeAmountMultiplier > 0 || (changeAmountMultiplier == 0 && previousChangeAmountMultiplier > 0))
				value.SetValue(value.valueRange.min);
			else
				value.SetValue(value.valueRange.max);
		}
		
		public void JumpToEnd ()
		{
			if (changeAmountMultiplier > 0 || (changeAmountMultiplier == 0 && previousChangeAmountMultiplier > 0))
				value.SetValue(value.valueRange.max);
			else
				value.SetValue(value.valueRange.min);
		}
		
		public void JumpToInitValue ()
		{
			value.SetValue(initValue);
		}
		
		public enum RepeatType
		{
			End,
			Loop,
			PingPong
		}
	}
}