import os
import importlib.util
import logging

logger = logging.getLogger(__name__)

def load_and_run_plugins(report):
    """
    动态加载 plugins/ 目录下的所有插件并执行它们的 run 函数
    
    Args:
        report (str): 生成的报告字符串，将被传递给每个插件的 run 函数
    
    Returns:
        str: 可能被插件修改后的报告
    """
    plugins_dir = os.path.join(os.getcwd(), 'plugins')
    
    # 确保插件目录存在
    if not os.path.exists(plugins_dir):
        os.makedirs(plugins_dir, exist_ok=True)
        return report
    
    plugins_files = [f for f in os.listdir(plugins_dir) 
                    if f.endswith('.py') and not f.startswith('__')]
    
    if not plugins_files:
        logger.info("No plugins found")
        return report
    
    logger.info(f"Found {len(plugins_files)} plugins")
    
    modified_report = report
    for plugin_file in plugins_files:
        plugin_name = os.path.splitext(plugin_file)[0]
        plugin_path = os.path.join(plugins_dir, plugin_file)
        
        try:
            # 动态加载模块
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            
            # 检查模块是否有 run 函数
            if hasattr(plugin_module, 'run') and callable(plugin_module.run):
                logger.info(f"Executing plugin: {plugin_name}")
                # 执行插件的 run 函数，并获取可能修改后的报告
                try:
                    result = plugin_module.run(modified_report)
                    if isinstance(result, str):
                        modified_report = result
                        logger.debug(f"Plugin {plugin_name} has modified the report")
                    else:
                        logger.debug(f"Plugin {plugin_name} run finished")
                except Exception as e:
                    logger.error(f"Plugin {plugin_name} run error: {e}")
            else:
                logger.warning(f"Plugin {plugin_name} is missing a callable `run` function")
        
        except Exception as e:
            logger.error(f"Error executing plugin {plugin_name}: {str(e)}", exc_info=True)
    
    return modified_report 