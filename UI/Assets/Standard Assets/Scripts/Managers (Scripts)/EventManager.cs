using System;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HolyBlender
{
	public class EventManager : SingletonUpdateWhileEnabled<EventManager>
	{
		public static List<Event> events = new List<Event>();

		public override void DoUpdate ()
		{
			for (int i = 0; i < events.Count; i ++)
			{
				Event _event = events[i];
				if (Time.timeSinceLevelLoad >= _event.time)
				{
					_event.onEvent ();
					events.RemoveAt(i);
					if (events.Count == 0)
					{
						enabled = false;
						return;
					}
					i --;
				}
			}
		}

		public static void AddEvent (Action action, float time)
		{
			events.Add(new Event(action, time));
			Instance.enabled = true;
		}

		public struct Event
		{
			public Action onEvent;
			public float time;

			public Event (Action onEvent, float time)
			{
				this.onEvent = onEvent;
				this.time = time;
			}
		}
	}
}