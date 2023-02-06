# Generated by Django 4.1 on 2023-01-16 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer", models.TextField(verbose_name="回答の内容")),
            ],
            options={
                "verbose_name_plural": "回答",
            },
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "c_id",
                    models.AutoField(
                        primary_key=True, serialize=False, verbose_name="企業ID"
                    ),
                ),
                (
                    "c_name",
                    models.CharField(max_length=100, unique=True, verbose_name="企業名"),
                ),
            ],
            options={
                "verbose_name_plural": "企業",
            },
        ),
        migrations.CreateModel(
            name="CompanyAnalysis",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "establishment",
                    models.DateField(
                        default="2000-01-01", null=True, verbose_name="設立年月日"
                    ),
                ),
                (
                    "location",
                    models.CharField(max_length=50, null=True, verbose_name="所在地"),
                ),
                ("capital", models.PositiveIntegerField(null=True, verbose_name="資本金")),
                ("sales", models.PositiveIntegerField(null=True, verbose_name="売上高")),
                ("emp_no", models.PositiveIntegerField(null=True, verbose_name="従業員数")),
                (
                    "representative",
                    models.CharField(max_length=50, null=True, verbose_name="代表者"),
                ),
                ("content", models.TextField(null=True, verbose_name="事業内容")),
                (
                    "url",
                    models.CharField(
                        default="https://",
                        max_length=50,
                        null=True,
                        verbose_name="参考url",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="登録日時"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新日時"),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pajamanApp.company",
                        verbose_name="企業名",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザ名",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "企業詳細",
            },
        ),
        migrations.CreateModel(
            name="Personality",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "q_id",
                    models.IntegerField(
                        primary_key=True, serialize=False, verbose_name="質問ID"
                    ),
                ),
                ("question", models.TextField(verbose_name="質問の内容")),
            ],
            options={
                "verbose_name_plural": "質問",
            },
        ),
        migrations.CreateModel(
            name="Self",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pajamanApp.answer",
                        verbose_name="回答",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pajamanApp.question",
                        verbose_name="質問",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "自己分析",
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "company_analysis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pajamanApp.companyanalysis",
                        verbose_name="企業分析",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "いいね",
            },
        ),
        migrations.CreateModel(
            name="ImageUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="icon/")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="登録日時"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "アイコン",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="コメント")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="作成日"
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pajamanApp.companyanalysis",
                        verbose_name="対象企業分析",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "コメント",
            },
        ),
        migrations.AddField(
            model_name="answer",
            name="personality",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="pajamanApp.personality",
                verbose_name="性格",
            ),
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="pajamanApp.question",
                verbose_name="回答ID",
            ),
        ),
    ]
