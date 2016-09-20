package net.GPCracker.interfaces
{
	import flash.events.IEventDispatcher;

	public interface ILoaderViewMeta extends IEventDispatcher
	{
		function as_createBattlePageComponent(componentAlias:String, componentClass:String, componentIndex:Number):void;
	}
}
