#if UNITY_EDITOR
using System;
using UnityEditor;

namespace HolyBlender
{
	public class SetScore : EditorScript
	{
		public uint score;

		public override void Do ()
		{
			_Do (score);
		}

		[MenuItem("Game/Set score to max")]
		static void _Do ()
		{
			_Do (uint.MaxValue);
		}

		static void _Do (uint score)
		{
			AccountManager.CurrentAccount.score = score;
		}
	}
}
#else
namespace HolyBlender
{
	public class SetScore : EditorScript
	{
	}
}
#endif