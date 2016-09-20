package net.GPCracker.panels
{
	import net.GPCracker.panels.TextPanel;

	public function getPanelClassReference(classAlias:String):Class
	{
		var classReference:Class = null;
		switch (classAlias)
		{
			case "TextPanel": classReference = TextPanel; break;
		}
		return classReference;
	}
}
