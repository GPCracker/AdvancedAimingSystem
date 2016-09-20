package net.GPCracker
{
	import flash.display.DisplayObjectContainer;
	import net.wg.infrastructure.base.AbstractView;
	import net.wg.gui.battle.random.views.BattlePage;
	import net.GPCracker.meta.LoaderViewMeta;
	import net.GPCracker.interfaces.ILoaderViewMeta;
	import net.GPCracker.panels.getPanelClassReference;

	public class LoaderView extends LoaderViewMeta implements ILoaderViewMeta
	{
		public function LoaderView()
		{
			super();
			return;
		}

		private function getBattlePage():BattlePage
		{
			var battleApp:DisplayObjectContainer = stage.getChildByName("root1") as DisplayObjectContainer;
			if (battleApp)
			{
				var battleViews:DisplayObjectContainer = battleApp.getChildByName("views") as DisplayObjectContainer;
				if (battleViews)
				{
					var battlePage:BattlePage = battleViews.getChildByName("main") as BattlePage;
					if (battlePage)
					{
						return battlePage;
					}
				}
			}
			return null;
		}

		public function as_createBattlePageComponent(componentAlias:String, componentClass:String, componentIndex:Number):void
		{
			var battlePage:BattlePage = this.getBattlePage();
			var classReference:Class = getPanelClassReference(componentClass);
			if (battlePage && classReference)
			{
				BattlePage.prototype[componentAlias] = null;
				battlePage[componentAlias] = new classReference();
				battlePage[componentAlias].name = componentAlias;
				battlePage.addChildAt(battlePage[componentAlias], componentIndex);
				battlePage.registerFlashComponentS(battlePage[componentAlias], componentAlias);
			}
			return;
		}

		override protected function onPopulate():void
		{
			super.onPopulate();
			return;
		}

		override protected function onDispose():void
		{
			super.onDispose();
			return;
		}
	}
}
