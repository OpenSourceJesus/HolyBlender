using System;
using System.Diagnostics;

namespace Extensions
{
	public static class FlowOfControlExtensions
	{
		// public static Func<TResult> DoCallingMethodNext<TResult>(this Func<TResult> func)
		// {
		// 	Delegate output = Delegate.CreateDelegate(new Delegate(null, new StackTrace().GetFrame(1).GetMethod().Name));
		// 	return output.Invoke;
		// }

		public static Action DoCallingMethodNext (this Action action)
		{
			return () => { action(); new StackTrace().GetFrame(1).GetMethod().Invoke(null, null); };
		}

		public static Action<T> DoCallingMethodNext<T> (this Action<T> action)
		{
			return (T value) => { action(value); new StackTrace().GetFrame(1).GetMethod().Invoke(null, new object[] { value }); };
		}
	}
}