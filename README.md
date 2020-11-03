# 使用方法：
      （1）git clone 到本地
      （2）进入该文件夹（vancancyMigration的父文件夹），命令行输入“pip install .”
      （3）进入python交互界面
             3.1 from vacancyMigration.vanMig import vacancyMigration1
             3.2 motion = vacancyMigration1(cifFile='输入一个cif文件的路径')   //CONTCAR、POSCAR可以用VESTA转化成cif格式
             3.3 motion.migration_nsteps(center=57, nsteps=5)    // center是空位初始位置，nsteps是扩散步数
